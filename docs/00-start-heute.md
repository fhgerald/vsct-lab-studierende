# Start für Kleingruppen: Labor 1

Eine Seite für heute (Fr 16.10.2026): was das Ziel ist, wo ihr alles findet und wie ihr
sofort eine Energiegemeinschaft ansehen könnt.

## Ziel für heute

- [ ] **Team gefunden:** Infrastruktur, Energiegemeinschaft (Kleingruppe), Prognose oder Handelsplattform
- [ ] **Auftrag verstanden:** Was liefert euer Team bis zum Meilenstein M1 (~06.11.)? Siehe die Teamseite
- [ ] **Unterlagen gefunden:** dieses Repository, besonders [Überblick](01-ueberblick.md) und die Seite eures Teams
- [ ] **Eine Energiegemeinschaft angesehen:** mit dem Lese-Zugang unten
- [ ] **Fragen notiert:** für Labor 2 (~23.10.) und die Betreuung

Nicht Ziel für heute: eigene Mandanten, eigene Zugänge, Code. Die kommen nach der Gruppeneinteilung
zu Labor 2.

## Wo liegt was

| Was | Wo |
|---|---|
| Alle Unterlagen für Studierende | <https://github.com/fhgerald/vsct-lab-studierende> (öffentlich, ohne Anmeldung) |
| Überblick, Teams, Meilensteine, Termine | [Seite 1](01-ueberblick.md) |
| Zugang und Regeln | [Seite 2](02-zugang.md) |
| Fachliche Grundlagen, OBIS-Register | [Seite 3](03-energiegemeinschaft-fachlich.md) |
| Daten und Simulation | [Seite 4](04-daten-und-simulation.md) |
| Eure Teamseite | [Infrastruktur](07-team-infrastruktur.md) · [Energiegemeinschaft](08-team-energiegemeinschaft.md) · [Prognose](09-team-prognose.md) · [Handelsplattform](10-team-handelsplattform.md) |
| Fallen und Hilfe | [Seite 11](11-fallen-und-hilfe.md) |
| Energiegemeinschafts-App | `https://energy-community.machasing.com/<mandant>` |
| Allgemeine Tutorials (Englisch) | <https://docs.meshmakers.cloud> |

## Eine Energiegemeinschaft ansehen: der Lese-Zugang

Für heute gibt es **einen gemeinsamen Zugang zum Lesen** in zwei Referenzgemeinschaften mit
**simulierten Daten**. Persönliche Zugänge für euer Team folgen nach Labor 2.

| Gemeinschaft | Adresse | Preset |
|---|---|---|
| `eg-urstein` | `https://energy-community.machasing.com/eg-urstein` | `legacy`: 14 große Verbraucher, 3 PV, reiner Käufer |
| `eg-lehrende` | `https://energy-community.machasing.com/eg-lehrende` | `pv-dorf`: 30 Haushalte, 2 Betriebe, 12 PV-Anlagen, mittags Überschuss |

| | |
|---|---|
| Benutzername | `lesezugang` (in beiden Gemeinschaften derselbe) |
| Passwort | bekommt ihr **im Labor** von den Lehrenden (je Gemeinschaft ein eigenes) |

`eg-lehrende` ist die Spielwiese der Lehrenden und für Vorführungen gedacht. Ihr seht dort die
Daten, **ändert aber nichts**: Einstellungen und Resets sind den Lehrenden vorbehalten.

**Regeln für den Lese-Zugang**

- Er darf nur **ansehen**: Statistiken, Energiemengen, Zählpunkte, Kunden. Ändern geht nicht.
- Das Passwort gebt ihr nicht außerhalb des Kurses weiter und schreibt es nicht in ein Repo oder einen Chat.
- Sobald euer eigener Mandant bereit ist (die Infra-Gruppe baut ihn auf, spätestens nach Labor 2), wird der Zugang abgeschaltet.

**Was ihr damit machen könnt**

1. Meldet euch an und öffnet **Statistiken**. Wählt einen Zeitraum.
2. Lest ab: **Erzeugung**, **Überschuss** und **Erzeugung in EEG**. Die Kachel „Verbrauch“ zeigt das
   aus der Gemeinschaft Gedeckte (Register `G.03`), nicht den gesamten Verbrauch.
3. Rechnet den **Nutzungsgrad** nach: „Erzeugung in EEG“ geteilt durch „Erzeugung“.
4. Öffnet **Zählpunkte** und **Kunden**: wie viele Verbraucher und Erzeuger hat die Gemeinschaft?
5. Schreibt auf, was euch auffällt und was ihr für euer Team wissen wollt.

Für interessante Effizienzzahlen nehmt `eg-lehrende` (mittags viel Überschuss). `eg-urstein` ist als reiner
Käufer eher das Gegenbeispiel: Vergleicht beide.

## Wie es weitergeht

| Wann | Was |
|---|---|
| ~23.10. | **Labor 2:** Gruppeneinteilung, Mandanten und persönliche Benutzer, Einführung in Security |
| Ende Okt. | Datenvertrag Handel v0.1 |
| ~06.11. | **M1:** Plattform und Verträge stehen, Datenvertrag v1.0 |
| ~13.11. | **Labor 3:** Energiegemeinschaft fachlich |

Alle Termine mit „~“ sind Vorschläge.
