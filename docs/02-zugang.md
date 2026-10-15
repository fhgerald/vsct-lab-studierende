# 2 Zugang und Regeln

## Adressen

| Was | Adresse |
|---|---|
| Energiegemeinschafts-App | `https://energy-community.machasing.com/<tenant>` |
| Studio (Daten, Modelle, Archive, Pipelines) | `https://studio.machasing.com/<tenant>` |
| GraphQL-API | `https://assets.machasing.com/tenants/<tenant>/GraphQL` |
| GraphQL-Playground | `https://assets.machasing.com/tenants/<tenant>/graphql/playground` |
| MCP-Server für KI-Clients | `https://mcp.machasing.com/mcp` |
| Identity-Service (Anmeldung, Token) | `https://connect.machasing.com/` |
| Passwort ändern | `https://connect.machasing.com/<tenant>/manage/password` |

`<tenant>` ist der Mandant eurer Gemeinschaft, z. B. `eg-alpha`. Ihr bekommt ihn
zusammen mit eurem Benutzer, **direkt nach der Gruppeneinteilung zu Labor 2**.

## Benutzer

Jede Person hat einen persönlichen Benutzer im Mandanten der eigenen Gruppe
(Benutzername = FH-Kürzel). Das Initialpasswort bekommt ihr persönlich oder über
einen sicheren Kanal. **Ändert es beim ersten Login** über die Adresse oben.

## Kubernetes

Den Zugang zum Cluster bekommt ihr als **kubeconfig-Datei** für euren Namespace
`grp-<gruppe>`. Grenzen je Gruppe: 4 CPU, 8 GB RAM, 20 GB Speicher, 30 Pods,
genau ein LoadBalancer. Jeder Pod braucht `resources.limits`, sonst scheitert er
mit `pods forbidden: failed quota`.

## octo-cli einrichten

```bash
octo-cli -c AddContext -n fh-cloud-lab_<tenant> \
  -isu https://connect.machasing.com/ -asu https://assets.machasing.com/ \
  -bsu https://bot.machasing.com/ -csu https://communication.machasing.com/ \
  -tid <tenant>
octo-cli --context fh-cloud-lab_<tenant> -c LogIn -i
```

Mehr dazu im Tutorial
[Getting started](https://docs.meshmakers.cloud/docs/tutorials/gettingStarted).

## Was ihr dürft

Im **eigenen** Mandanten:

- Daten, Modelle, Archive, Dashboards und Berichte ansehen (Studio, App, GraphQL)
- Stammdaten anlegen und ändern: Kunden, Anlagen, Zählpunkte
  ([Seite 6](06-stammdaten-import.md))
- die Simulationseinstellungen eurer Gemeinschaft ändern und einen Reset
  beantragen ([Seite 4](04-daten-und-simulation.md))
- eigene Zähler anmelden und melden, sobald sie freigeschaltet sind
  ([Seite 5](05-eigene-zaehler.md))

**Nicht:** Benutzer anlegen, Rollen vergeben, Secrets verwalten, Archive löschen
oder aktivieren. In die Mandanten anderer Gruppen kommt ihr nicht. Die
Produkt-Abrechnung und die App gibt es als Referenz in `eg-urstein`; in euren
Mandanten ist die Produkt-Abrechnung nicht installiert, bewertet wird euer
eigener Dienst.

## Umgang mit Zugangsdaten

- Gebt Zugangsdaten nie weiter, auch nicht innerhalb der Gruppe.
- **Nie in ein Repository, einen Chat, ein Ticket oder eine KI-Unterhaltung:**
  Passwörter, Client-Secrets, Token, kubeconfig-Dateien.
- `octo-cli -c AuthStatus` **druckt euer Zugriffstoken**, und
  `~/.octo-cli/contexts.json` enthält es. Beides nie kopieren.
- Client-Secrets, die ihr von der Betreuung bekommt, gehören in Umgebungsvariablen
  oder in eine Datei außerhalb des Repos (Dateirechte 600).
- Wenn doch etwas durchgerutscht ist: sofort der Betreuung melden. Das Secret wird
  dann ausgetauscht; das ist kein Drama, solange ihr es schnell meldet.
