# 7 Team Infrastruktur

**Wer:** ein Team aus CYS und IIR (Auswahl im Labor 1), für alle Gruppen.

## Ziel

Ihr baut die Plattform, auf der alle anderen Teams ihre Dienste betreiben:
Kubernetes-Namespaces, Deployments, Zugriffsrechte (RBAC) gemeinsam mit dem
Security-Board, eine CI/CD-Vorlage und die Observability mit OpenTelemetry und
dash0. In der zweiten Hälfte geht es um Betrieb und Resilienz. OctoMesh könnt ihr
zur Datenintegration nutzen, müsst es aber nicht.

Die Basis (Kubernetes-Cluster, Ingress, Zertifikate, OctoMesh, Datenbanken)
betreibt die Lehre. Ihr arbeitet **auf** dieser Basis und beobachtet sie.

## Was ihr vorfindet

- Je Team einen Namespace `grp-<team>` mit Kontingent (4 CPU, 8 GB RAM, 20 GB
  Speicher, 30 Pods, 1 LoadBalancer); für euch selbst mehr (8 CPU, 16 GB, 50 GB,
  60 Pods). Zusätzlich Namespaces für AIT und je eine IMC-Plattform.
- Ingress und ein Wildcard-Zertifikat für `*.machasing.com`. Versteht, was schon
  da ist, statt es neu zu bauen.
- Zugang per kubeconfig und FH-VPN oder eduroam. Die Kubernetes-API ist nur dort
  erreichbar.

## Aufgaben nach Meilenstein

| Bis | Aufgaben | Ihr liefert |
|---|---|---|
| Labor 1 bis 2 | Zugang testen; vorhandenes Ingress und Zertifikat verstehen; Namens- und Hostnamenschema; Onboarding-Doku | Onboarding-Doku v1 (KW44) |
| **M1** | CI/CD-Vorlage (Build, Image, Deploy in `grp-<team>`, `resources.limits` gesetzt); dash0 und OTel für alle Team-Namespaces, Service-Namen je Dienst; Beispieldienst mit Trace | Vorlage, Beispieldienst in dash0, Dashboard je Team |
| **M2** | Teams beim ersten Deployment begleiten; Alarme; Ressourcen je Namespace beobachten | jedes Team hat mindestens einen Dienst über die Vorlage deployt |
| **M3** | Infrastruktur der drei Handelsplattformen mit den IMC-Gruppen (Namespaces, Ingress, Secrets); Lasttest der Handels-APIs und der Melde-Endpunkte (Richtwert: 200 Aufrufe in 60 s, p95 ≤ 2 s); durchgehender Trace von der Gemeinschaft bis zur Plattform | Lasttest-Protokoll, Trace-Nachweis |
| **M4** | Backup und Restore an eigenen Diensten und einem Testmandanten (nur gemeinsam mit der Lehre); Ausfallübungen mit Nachweis in dash0 (Plattform-Dienst weg während des Marktschlusses, Prognose-Dienst langsam); Runbook | Restore- und Ausfallbericht, Runbook |

## Hinweise

- Lasttests nur in Absprache und nicht während der Labortermine; das Cluster ist
  klein (drei Knoten).
- Zwischen Namespaces gibt es **nicht automatisch** eine Netzwerkgrenze. Das ist
  ein Thema für euch und das Security-Board.
- Die Lehre hebt die Plattform in **Upgrade-Fenstern** (geplant: 20. bis 23.11. und
  um den 11.12.). Ihr beobachtet dabei mit; danach gilt ein Freeze.

Zugang und Regeln: [Seite 2](02-zugang.md). Vorlesungsbezug: Kapitel 1, 2 B, 6 B
und der Gastvortrag dash0.
