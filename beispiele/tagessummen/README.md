# Beispiel: Tagessummen-Dienst auf Kubernetes

Für das Labor am **Mi 11.11.2026**. Ein kleiner Dienst in Python (FastAPI), der die
15-Minuten-Werte eurer Energiegemeinschaft über die GraphQL-API von OctoMesh liest
und je Kalendertag die Summe pro Register liefert. Ihr bringt ihn zuerst auf ein
**lokales Kubernetes (kind)**, macht ihn dort kaputt und seht zu, wie Kubernetes
reagiert. Danach kann dasselbe Manifest in euren Namespace `grp-<team>` im Lab-Cluster.

**Warum gerade dieser Dienst:** Bis **M2 (20.11.)** liefert jede Gemeinschaft eine
rollengeschützte Schnittstelle „Tagessummen/Tagesprofil“ an das Prognose-Team
([Seite 8](../../docs/08-team-energiegemeinschaft.md)). Das hier ist ein
**Startpunkt, kein Vertrag**: Felder, Einheiten, Fehlerfälle und die richtige
Authentisierung vereinbart ihr selbst mit AIT (siehe „Was für M2 noch fehlt“).

## Was ihr vorher installiert

| Werkzeug | Prüfen mit |
|---|---|
| Docker Desktop (oder Podman) | `docker run --rm hello-world` |
| kind | `kind version` (<https://kind.sigs.k8s.io/docs/user/quick-start/#installation>) |
| kubectl | `kubectl version --client` |

Einmal vor dem Labor ausprobieren: `kind create cluster --name probe` und danach
`kind delete cluster --name probe`. Wenn das nicht geht, sagt es vorher der Betreuung.

## Was ihr im Labor bekommt

- **Client-ID und Client-Secret** eines Clients mit der Rolle `StreamDataReader`, je Team ein eigener
- Mandant für die Übung ist **`eg-lehrende`** (simulierte Daten, `pv-dorf`). Sobald es den Mandanten eurer
  Gemeinschaft gibt, tragt ihr ihn in `k8s/10-configmap.yaml` ein und bekommt dort einen eigenen Client.

Das Secret ist ein Zugangsdatum: nie ins Repo, in einen Chat oder eine KI-Unterhaltung
([Seite 2](../../docs/02-zugang.md)).

## Aufbau

```
app/          main.py, requirements.txt, Dockerfile
kind/         cluster.yaml: ein Steuerknoten, zwei Worker
k8s/          00-namespace.yaml   Namespace grp-uebung mit demselben Kontingent wie im Lab-Cluster
              10-configmap.yaml   Mandant, Zeitzone, Adressen (keine Geheimnisse)
              20-deployment.yaml  der Dienst: Limits, Probes, Secret als Umgebungsvariablen
              30-service.yaml     stabiler Name "tagessummen" im Cluster
              uebung-*.yaml       für die Übungen
cluster/      ingress.yaml        nur für den Lab-Cluster
```

| Schnittstelle | |
|---|---|
| `GET /tagessummen?von=2026-10-24&bis=2026-10-25` | je Tag: Anzahl Viertelstunden, je Register kWh und Anzahl Werte; Header `X-API-Key` Pflicht; höchstens 31 Tage |
| `GET /healthz` | Lebt der Prozess? (Liveness) |
| `GET /readyz` | Konfiguration vollständig und Token von OctoMesh zu bekommen? (Readiness) |

## Schritt für Schritt (kind)

Alle Befehle aus diesem Ordner (`beispiele/tagessummen`).

```bash
# 1 Cluster anlegen (dauert 1–2 Minuten)
kind create cluster --name vsct --config kind/cluster.yaml
kubectl get nodes

# 2 Image bauen und ins kind-Cluster laden (kein Registry nötig)
docker build -t ghcr.io/fhgerald/tagessummen:1.0 app
docker build -t ghcr.io/fhgerald/tagessummen:1.1-fehler --build-arg APP_VERSION=1.1-fehler app
kind load docker-image --name vsct ghcr.io/fhgerald/tagessummen:1.0 ghcr.io/fhgerald/tagessummen:1.1-fehler

# 3 Namespace mit Kontingent, und ab jetzt dort arbeiten
kubectl apply -f k8s/00-namespace.yaml
kubectl config set-context --current --namespace=grp-uebung

# 4 Secret anlegen: Werte eintippen, nicht in eine Datei im Repo schreiben
kubectl create secret generic tagessummen \
  --from-literal=OCTO_CLIENT_ID='<client-id>' \
  --from-literal=OCTO_CLIENT_SECRET='<client-secret>' \
  --from-literal=API_KEY='<denkt-euch-einen-aus>'

# 5 Ausrollen (Mandant steht in k8s/10-configmap.yaml, für die Übung eg-lehrende)
kubectl apply -f k8s/10-configmap.yaml -f k8s/20-deployment.yaml -f k8s/30-service.yaml
kubectl get pods -w          # warten bis READY 1/1, dann Strg+C

# 6 Aufrufen
kubectl port-forward svc/tagessummen 8080:80
# in einem zweiten Terminal:
curl -H "X-API-Key: <euer-schluessel>" "localhost:8080/tagessummen?von=2026-10-24&bis=2026-10-25"
```

Bleibt der Pod auf `READY 0/1`: `kubectl describe pod -l app=tagessummen` (Events unten)
und `kubectl logs -l app=tagessummen`. Häufig: Secret fehlt, Tippfehler in Client-ID oder
Mandant.

## Übungen

**Pflicht**

- [ ] Der Dienst läuft (`READY 1/1`) und liefert Tagessummen für euren Mandanten.
- [ ] Ohne `X-API-Key` kommt `401`.
- [ ] `kubectl apply -f k8s/uebung-ohne-limits.yaml`: Was sagt Kubernetes, und warum? (`kubectl describe quota`)

**Verstehen** (mindestens drei)

- [ ] **Selbstheilung:** `kubectl delete pod -l app=tagessummen` und sofort `kubectl get pods -w`.
- [ ] **Skalieren:** `kubectl scale deploy/tagessummen --replicas=2`, dann
      `kubectl apply -f k8s/uebung-aufrufer.yaml` und `kubectl logs -f aufrufer`. Der Header `x-pod`
      zeigt, welcher Pod antwortet. Warum liefern beide dasselbe? (Wo liegt der Zustand?)
- [ ] **Knotenausfall:** Mit zwei Repliken und laufendem `aufrufer`: `kubectl get pods -o wide`, einen
      Worker stoppen, auf dem ein `tagessummen`-Pod läuft, aber nicht der `aufrufer`
      (`docker stop vsct-worker2`). Logs beobachten: Wie lange gibt es Fehler, wann kommt der Ersatz-Pod?
      Danach `docker start vsct-worker2`. Was steuern die `tolerations` im Deployment?
- [ ] **Fehlerhaftes Update und Rollback:**
      `kubectl set image deploy/tagessummen tagessummen=ghcr.io/fhgerald/tagessummen:1.1-fehler`.
      Das Update läuft sauber durch, alle Probes sind grün. Fragt den **25.10.2026** ab und vergleicht
      mit Version 1.0. Was ist falsch? Dann `kubectl rollout undo deploy/tagessummen`.
- [ ] **Readiness:** Secret mit falschem Client-Secret neu anlegen und Pods neu starten
      (`kubectl rollout restart deploy/tagessummen`). Was passiert mit den alten Pods, solange die neuen
      nicht bereit sind?

**Für Schnelle**

- [ ] Ein CronJob, der jeden Morgen die Tagessummen von gestern abruft und ins Log schreibt.
- [ ] Skizze: Wie sähe eine NetworkPolicy aus, die nur den Dienst von AIT an `tagessummen` lässt?
      (Hinweis: Das Standardnetz von kind setzt NetworkPolicies nicht durch.)

## Fragen zum Nachdenken

1. Am 25.10.2026 endete die Sommerzeit. Wie viele Viertelstunden hat dieser Tag in Wien, und was
   passiert, wenn man in UTC-Tagen summiert?
2. `/readyz` hängt davon ab, dass OctoMesh ein Token ausgibt. Was passiert mit allen Repliken, wenn
   der Identity-Dienst fünf Minuten ausfällt? Ist das gewollt?
3. Warum verlegt Kubernetes Pods von einem ausgefallenen Knoten standardmäßig erst nach 5 Minuten?

## In den Lab-Cluster (`grp-<team>`)

Erst wenn es lokal läuft, und nur mit eurer kubeconfig.

1. Das Image muss aus einer Registry kommen, die der Cluster erreicht. Das Beispiel-Image liegt unter
   `ghcr.io/fhgerald/tagessummen` (öffentlich). Für euren eigenen Dienst nutzt ihr die CI/CD-Vorlage des
   Infra-Teams.
2. `kubectl config set-context --current --namespace=grp-<team>`, Secret wie oben anlegen, dann
   `k8s/10-configmap.yaml`, `k8s/20-deployment.yaml`, `k8s/30-service.yaml` anwenden. **Nicht**
   `00-namespace.yaml`, den Namespace gibt es schon.
3. In `cluster/ingress.yaml` `<team>` ersetzen und anwenden. Dann antwortet der Dienst unter
   `https://<team>-tagessummen.machasing.com/`.
4. Den Knotenausfall und den Pod ohne Limits übt ihr **nur lokal**, nie im Lab-Cluster.

## Was für M2 noch fehlt (eure Aufgabe)

- **Vertrag mit AIT:** Welche Felder, Einheiten, Zeitzone, Zeitraum, was bei fehlenden oder
  nachgemeldeten Werten (Datenqualität)? Tagessummen oder Tagesprofil (96 Werte)?
- **Rollengeschützt:** Der API-Schlüssel ist nur ein Platzhalter. Richtig ist, das OctoMesh-Token des
  Aufrufers zu prüfen (Aussteller, Mandant, Rolle) oder die Schnittstelle als Pipeline mit
  `requiredRoles` zu bauen.
- **Fachlich:** Welche Register braucht AIT wirklich? Keine Daten einzelner Mitglieder herausgeben,
  15-Minuten-Lastgänge sind personenbezogen.
- **Beobachtbar:** OpenTelemetry und dash0, wie es das Infra-Team vorgibt.

## Aufräumen

```bash
kind delete cluster --name vsct
```
