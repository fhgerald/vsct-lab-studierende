# Labor Verteilte Systeme und Cloud-Technologien – Unterlagen für Studierende

FH Salzburg, WS 2026/27. Hier steht, was ihr im Labor braucht: Zugänge, eure
Aufgaben je Team, die Daten und die Schnittstellen. Die Seiten sind auf Deutsch;
die allgemeinen OctoMesh-Tutorials sind auf Englisch online
(<https://docs.meshmakers.cloud>).

> **Stand 15.10.2026, Entwurf zum Kickoff am 16.10.** Termine mit „~“ sind
> Vorschläge. Was noch nicht entschieden ist, steht auf der jeweiligen Seite
> unter „Noch offen“.

## Heute (Labor 1)

**Start für Kleingruppen:** [Ziel für heute, wo liegt was, Lese-Zugang zu einer Energiegemeinschaft](docs/00-start-heute.md)

## Wo ihr anfangt

| Ihr seid … | Lest zuerst |
|---|---|
| alle | [1 Überblick](docs/01-ueberblick.md), [2 Zugang und Regeln](docs/02-zugang.md) |
| Team **Infrastruktur** (CYS/IIR) | [7 Team Infrastruktur](docs/07-team-infrastruktur.md) |
| Team **Energiegemeinschaft** (CYS/IIR, je Kleingruppe) | [8 Team Energiegemeinschaft](docs/08-team-energiegemeinschaft.md), dazu 3 bis 6 |
| Team **Prognose** (AIT) | [9 Team Prognose](docs/09-team-prognose.md) |
| Team **Handelsplattform** (IMC) | [10 Team Handelsplattform](docs/10-team-handelsplattform.md) |
| steckt fest | [11 Fallen und Hilfe](docs/11-fallen-und-hilfe.md) |

## Inhalt

1. [Überblick](docs/01-ueberblick.md): Idee des Labors, Teams, Datenfluss, Meilensteine
2. [Zugang und Regeln](docs/02-zugang.md): Adressen, Benutzer, octo-cli, Kubernetes, Umgang mit Zugangsdaten
3. [Energiegemeinschaften fachlich](docs/03-energiegemeinschaft-fachlich.md): Grundidee, Verteilung D+1, Register, Kennzahlen
4. [Daten und Simulation](docs/04-daten-und-simulation.md): was vorbereitet ist, Einstellungen, Reset, Presets
5. [Eigene Zähler melden](docs/05-eigene-zaehler.md): Token, Routen, Beispiele (ab Labor 4b)
6. [Stammdaten importieren](docs/06-stammdaten-import.md): Kunden, Anlagen, Zählpunkte per Skript
7. [Team Infrastruktur](docs/07-team-infrastruktur.md)
8. [Team Energiegemeinschaft](docs/08-team-energiegemeinschaft.md)
9. [Team Prognose (AIT)](docs/09-team-prognose.md)
10. [Team Handelsplattform (IMC)](docs/10-team-handelsplattform.md): inkl. gemeinsamer Datenvertrag
11. [Fallen und Hilfe](docs/11-fallen-und-hilfe.md)
12. [Was läuft im Kubernetes-Cluster?](docs/12-kubernetes-uebersicht.md): Übersichtsgrafik

Im Ordner `scripts/` liegt `import-stammdaten.py`, in `templates/stammdaten/`
liegen die Vorlagen dazu. Das Infra-Team arbeitet zusätzlich in einem eigenen, privaten
Repository (Einladung durch die Betreuung).

## Wichtigste Regel

**Zugangsdaten gehören nie in dieses Repo, in einen Chat, ein Ticket oder eine
KI-Unterhaltung:** keine Passwörter, keine Client-Secrets, keine Token, keine
kubeconfig-Dateien. Näheres in [Zugang und Regeln](docs/02-zugang.md).
