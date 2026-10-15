# 6 Stammdaten importieren

Anleitung für die Gruppen: eigene Kunden, Anlagen und Zählpunkte in die
Energiegemeinschaft der Gruppe bringen. Ein Excel-Add-in gibt es im Labor
nicht, dafür das Skript `scripts/import-stammdaten.py`.

## Was man braucht

- Python 3.9 oder neuer. Für `.xlsx` zusätzlich `openpyxl`
  (`python3 -m pip install openpyxl`); CSV geht ohne.
- `octo-cli` und einen Benutzer im Tenant der eigenen Gemeinschaft ([Seite 2](02-zugang.md)).
- Den Tenant-Namen eurer Gemeinschaft, z. B. `eg-alpha`.

Einmal einen octo-cli-Kontext anlegen und anmelden:

```bash
octo-cli -c AddContext -n fh-cloud-lab_eg-alpha \
  -isu https://connect.machasing.com/ -asu https://assets.machasing.com/ \
  -bsu https://bot.machasing.com/ -csu https://communication.machasing.com/ \
  -tid eg-alpha
octo-cli --context fh-cloud-lab_eg-alpha -c LogIn -i
```

Das Skript holt das Zugriffstoken aus diesem Kontext und erneuert es bei
Bedarf. Es gibt das Token nie aus. Selbst nie `octo-cli -c AuthStatus` ohne
Umleitung in ein Protokoll oder einen Chat kopieren: der Befehl druckt das
Token.

## Die vier Dateien

Vorlagen mit erfundenen Beispielzeilen liegen in `templates/stammdaten/` dieses Repos.
Kopieren, Beispielzeilen ersetzen, importieren. Trennzeichen `;` (so speichert
ein deutsches Excel CSV), `,` geht auch. Kodierung UTF-8.

| Datei | Typ | Schlüssel (macht eine Zeile eindeutig) |
|---|---|---|
| `kunden.csv` | Mitglied der Gemeinschaft | `customerNumber` |
| `anlagen.csv` | Anlage (Gebäude, Standort) eines Kunden | `name` + Kundennummer |
| `verbraucher.csv` | Zählpunkt Bezug | `meteringPointNumber` |
| `erzeuger.csv` | Zählpunkt Einspeisung | `meteringPointNumber` |

Die Reihenfolge zählt: Anlagen verweisen auf Kunden, Zählpunkte auf Anlagen.
`alle` hält sie ein.

Die Kopfzeile besteht aus den Attributpfaden von OctoMesh. Welche Spalten
gelten, zeigt das Skript selbst:

```bash
scripts/import-stammdaten.py -c fh-cloud-lab_eg-alpha spalten
```

Pflichtfelder (sonst lehnt der Server die Zeile ab):

| Typ | Pflicht |
|---|---|
| Kunde | `customerNumber`, Adresse (`contact.address.street`, `.zipcode`, `.cityTown`, `.nationalCode`), `taxProcedureCreditNote` |
| Anlage | `name`, Kundennummer, `facilityType`, Adresse (`address.*`), **PLZ des Orts** `parent.basicCity->zipcode` |
| Zählpunkt | `meteringPointNumber`, `name`, Anlagenname + Kundennummer; Erzeuger zusätzlich `productionType` |

Werte für Auswahlfelder (Name oder Zahl):

| Spalte | Werte |
|---|---|
| `contact.legalEntityType` | NaturalPerson (0), LegalPerson (1), Company (2), LocalAuthority (3) |
| `contact.salutation` | Unknown (0), Male (1), Female (2), NonBinary (3) |
| `taxProcedureCreditNote` | SmallBusinessOwners (0), ReverseCharge (1), NoTaxProcedure (2), FarmerTaxProcedure (3) |
| `facilityType` | Unknown (0), Household (1), Business (2), Industry (3), PublicBuilding (4), Storage (5) |
| `productionType` | Unknown (0), Solar (1), HEP (2, Wasserkraft), Wind (3), Other (4), Biomass (5), CHP (6) |
| `carrierType` | Unknown (0), Electricity (1), Gas (2). Optional, Standard Electricity |

Einheiten: `energyConsumption` in kWh pro Jahr, `energyProductionCapacity`
in kWp. Zahlen mit Komma oder Punkt. Optional für Zählpunkte:
`partitionFactor` (Teilnahmefaktor in Prozent).

## Ablauf

```bash
# 1. Probelauf: zeigt, was angelegt oder geändert würde, schreibt nichts
scripts/import-stammdaten.py -c fh-cloud-lab_eg-alpha alle meine-daten/ --probelauf

# 2. Import
scripts/import-stammdaten.py -c fh-cloud-lab_eg-alpha alle meine-daten/

# einzelne Datei oder eine Excel-Mappe mit den Blättern
# Kunden / Anlagen / Verbraucher / Erzeuger
scripts/import-stammdaten.py -c fh-cloud-lab_eg-alpha kunden meine-daten/kunden.csv
scripts/import-stammdaten.py -c fh-cloud-lab_eg-alpha alle stammdaten.xlsx
```

`meine-daten/` ist ein Ordner mit `kunden.csv`, `anlagen.csv`,
`verbraucher.csv`, `erzeuger.csv` (einzelne dürfen fehlen).

Nach dem Import trägt das Skript in die Spalte `rtId` die Kennung jedes
Objekts ein. Ein zweiter Lauf mit derselben Datei ändert nichts. Um etwas zu
ändern: Wert in der Datei ändern, erneut importieren; das Skript schickt nur
geänderte Zeilen und zeigt vorher alt und neu.

## Regeln

- **`rtId` leer** = neu anlegen, **`rtId` gefüllt** = dieses Objekt ändern.
  Fehlt die rtId, sucht das Skript zuerst über den Schlüssel; gibt es das
  Objekt schon, wird es geändert statt doppelt angelegt.
- **rtIds nie zwischen Tenants kopieren.** Eine fremde rtId meldet das Skript
  als Fehler; dann die Spalte leeren.
- **Leere Zelle löscht den Wert.** Eine leere Verweis-Spalte (mit `->`) lässt
  die bestehende Zuordnung dagegen unverändert.
- **Kundennummer immer ausfüllen.** Der Server vergibt beim Anlegen eine eigene
  Nummer aus einem Zähler; das Skript setzt sofort den Wert aus der Datei, damit
  Anlagen und Zählpunkte den Kunden finden.
- **Zählpunkt umhängen:** Anlagenname und Kundennummer ändern, importieren.
- **Löschen** kann das Skript nicht. Das geht in der Oberfläche.
- Spalten, die mit `#` oder `_` beginnen, ignoriert das Skript (für Notizen).
- Prüft eine Datei Fehler, wird aus ihr nichts geschrieben und die folgenden
  Dateien werden übersprungen.

## Häufige Fehler

| Meldung | Ursache, Abhilfe |
|---|---|
| `Kunde 1234 gibt es nicht` | Kunden zuerst importieren oder Tippfehler in der Kundennummer |
| `PLZ … steht nicht im Ortsverzeichnis` | PLZ prüfen; es zählt die PLZ des Orts in Österreich |
| `PLZ … gehört zu 2 Orten` | 5440, 5441 und 3494 sind mehrdeutig. Diese Anlage in der Oberfläche anlegen und dort den Ort wählen |
| `Im Tenant gibt es kein Ortsverzeichnis` | Betreuung informieren; das Ortsverzeichnis gehört zum Aufbau der Gemeinschaft |
| `Anlage '…' von Kunde … gibt es nicht` | Anlagen zuerst importieren; Name und Kundennummer müssen genau passen |
| `… gibt es nicht. Erlaubt: …` | Wert eines Auswahlfelds falsch geschrieben |
| `Anmeldung für Kontext … ungültig` | `octo-cli --context <kontext> -c LogIn -i` |
| `HTTP 401` / `HTTP 403` | Benutzer gehört nicht zum Tenant oder falscher Kontext |
| `Der Server hat die Anfrage abgelehnt` | Text darunter lesen: meist ein fehlendes Pflichtfeld. Nichts aus dem Block wurde angelegt |
