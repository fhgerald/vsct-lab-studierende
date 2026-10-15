# 4 Daten und Simulation

## Was in eurer Gemeinschaft vorbereitet ist

- **Stammdaten aus einem Preset:** Mitglieder, Anlagen, Zählpunkte, Preise. Jede
  Gruppe bekommt ein anderes Preset, damit sich die Gemeinschaften unterscheiden
  (manche haben Überschuss, andere Bedarf).
- **Zwei Jahre 15-Minuten-Werte** bis zum Vortag des Aufbaus. Danach rechnet die
  Simulation jeden Tag den Vortag weiter.
- **Verteilung D+1:** Jeden Tag wird der Vortag eingefroren und die Energie
  innerhalb der Gemeinschaft verteilt, wie es der Netzbetreiber bei einer echten
  Gemeinschaft täte. Meldeschluss je Tag ist 06:00 Wiener Zeit am Folgetag.
- **Ortsverzeichnis Österreich** (nötig für eigene Anlagen).

Die Simulation erzeugt Viertelstundenwerte für Verbrauch (nach den Lastprofilen
H0, G0 und L0) und Erzeugung (nach einer PV-Kurve). **Noch nicht** enthalten:
Wetter, Rauschen, Wärmepumpe, E-Auto. Wetter und Rauschen folgen mit einem
späteren Upgrade (siehe Termine).

## Wo die Daten liegen

| Was | Wo |
|---|---|
| Mitglieder, Anlagen, Zählpunkte | Runtime-Entitäten, Typen `EnergyCommunity/Customer`, `Basic.Energy/OperatingFacility`, `EnergyCommunity/Consumer`, `EnergyCommunity/Producer` |
| Je Zählpunkt und Register ein Anker | `Basic.Energy/EnergyMeasurement` mit `obisCode` |
| 15-Minuten-Werte | Archiv `ec0000000000000000000a01` (`energy-measurements`) |
| Summen je Stunde, Tag, Woche, Monat, Jahr | Rollup-Archive `ec0000000000000000000a02` bis `…a06` |

Für Auswertungen über Monate sind die Rollups der richtige Einstieg. Die Register
(`G.01`, `G.03`, `G.01T`, `P.01T`) erklärt [Seite 3](03-energiegemeinschaft-fachlich.md).

## Einstellungen ändern

Im Studio, Daten-Explorer, Typ `EnergyCommunity/SimulationSettings`. Einstellungen
sind **Revisionen**: Für einen Tag gilt die Revision mit dem jüngsten
`EffectiveFrom`, das nicht nach diesem Tag liegt. Eine Änderung heißt also: **neue
Revision anlegen**, nicht die alte bearbeiten. Rückwirkend geht nicht.

| Feld | Wirkung |
|---|---|
| `EffectiveFrom` | ab wann die Revision gilt |
| `ConsumptionFactor` | Verbrauch skalieren (0,5 bis 2) |
| `PvCapacityFactor` | PV-Leistung skalieren (0 bis 3) |
| `PvSpecificYield` | Ertrag in kWh/kWp und Jahr (Standard 1.050) |
| `Seed` | andere, aber reproduzierbare Streuung |
| `Noise`, `Weather` | Rauschen und Wetter, wirken erst nach dem Upgrade |

Gleiche Einstellungen ergeben bitgleiche Daten.

## Zurücksetzen (Reset)

Wer die Vergangenheit mit neuen Einstellungen sehen will, legt einen
**Reset-Auftrag** an (`EnergyCommunity/SimulationResetRequest`, `Mode` = `Values`
oder `Full`) und gibt der Betreuung Bescheid.

| Modus | Wirkung | Dauer (Richtwert) |
|---|---|---|
| `Values` | Mitglieder bleiben, alle Werte werden neu gerechnet | 90 Tage ≈ 5 min |
| `Full` | Mitglieder und Werte neu, auch mit anderem Preset | 730 Tage ≈ 15 bis 25 min |

`Full` dürft ihr nur bis zum Tag vor Labor 4 beantragen. **Achtung:** Bei `Full`
sind auch Werte weg, die ihr für eigene Zähler gemeldet habt.

## Presets

Richtwerte je Kalenderjahr; im Sommer und Winter unterscheiden sie sich deutlich.

| Preset | Zusammensetzung | Deckungsgrad D | Überschussquote U | am Markt |
|---|---|---|---|---|
| `legacy` | 14 große Verbraucher, 3 PV | 14–19 % | ≤ 1 % | Käufer |
| `pv-dorf` | 30 Haushalte, 2 Betriebe, 12 × PV 15 kWp | 40–55 % | 55–68 % | mittags Verkäufer, abends Käufer |
| `gewerbepark` | 8 Betriebe, 4 Haushalte, 4 × PV 100 kWp | 55–75 % | 12–35 % | eher Käufer |
| `landwirtschaft` | 10 Höfe, 15 Haushalte, 6 × PV 30 kWp | 30–42 % | 58–70 % | mittags Verkäufer |
| `stadtblock` | 60 Haushalte, 1 × PV 20 kWp | 10–18 % | ≤ 3,5 % | reiner Käufer |
| `wasserkraft-tal` | 25 Haushalte, 2 Betriebe, Kleinwasserkraft + PV | 65–82 % | 25–40 % | Nachtverkäufer (Werte nach dem Upgrade) |

## Abfragen: worauf ihr achten müsst

- **Zeitzonen.** Archive speichern UTC. Ein Tag der Gemeinschaft beginnt um
  Mitternacht Wiener Zeit (`22:00Z` im Sommer, `23:00Z` im Winter).
- **15-Minuten-Raster.** Abfragen und Meldungen immer auf `:00`, `:15`, `:30`,
  `:45` legen.
- **Attribute immer explizit anfordern.** Wer bei generischen GraphQL-Abfragen
  (`runtimeEntities`) `attributeNames` weglässt, bekommt alle Attribute.
- **GraphQL-Fehler kommen mit HTTP 200.** Immer das Feld `errors` in der Antwort
  prüfen.

Weiterführend: Tutorial
[Accessing data](https://docs.meshmakers.cloud/docs/tutorials/accessingData).
