# 10 Team Handelsplattform (IMC)

**Wer:** drei Gruppen aus IMC. Jede Gruppe baut **eine eigene Handelsplattform**.
Alle drei nutzen **denselben Datenvertrag**, dürfen aber verschiedene interne
Architekturen und Algorithmen verwenden.

## Ziel

Eine tagesbasierte Handelsplattform: Sie kauft Energie von Gemeinschaften an,
verkauft sie an Gemeinschaften mit Bedarf und deckt Fehlmengen über ein teures,
simuliertes **Reservekraftwerk**. Die Plattform ist selbst Vertragspartnerin.

**Mengenlogik** (für den Liefertag d, Angebote s, Bedarfe D):
S = Σ Angebote, D = Σ Bedarfe.
Die Gemeinschaften liefern E_EG = min(S, D), das Reservekraftwerk
E_Reserve = max(D − S, 0).

**Preis und Zuteilung wählt und begründet jede Gruppe selbst.** Im Standardfall
nutzt die Plattform alle Angebote und lässt die teurere Reserve den Fehlbetrag
decken. Bei Überangebot kauft sie nur die benötigte Menge und teilt nach einer
**eigenen, dokumentierten Regel** zu (z. B. proportional oder nach Preisrangfolge;
keine ist vorgeschrieben). Die Formeln in den Vorlesungsfolien sind ein
**Rechenbeispiel**, kein Pflichtmodell. Gleiche Eingaben dürfen also zu
verschiedenen Preisen und Einzelzuteilungen führen.

## Nicht Teil der Plattform

- direkte Smart-Meter- oder AIT-Anbindung
- Verbrauchs- oder Erzeugungsprognosen
- Handel innerhalb einer Gemeinschaft
- direkter Handel zwischen Gemeinschaften
- reale Netzsteuerung, Stromlieferung oder Zahlungsabwicklung

## Datenvertrag Handel

Alle drei Plattformen erfüllen denselben Austauschvertrag. Termine: **Version 0.1
Ende Oktober, Version 1.0 Anfang November (bis M1)**. Ihr schreibt ihn **gemeinsam**;
wer ihn pflegt und moderiert, klären die Lehrenden (noch offen).

Inhalt laut Folien:

- **Objekte:** Energiegemeinschaft und Handelsstatus; Tagesangebot oder Tagesbedarf;
  Handelsauftrag und Marktschluss; Handelsabschluss und Tagesabrechnung; Preise,
  Zuteilung und Fehlerstatus. Beispielobjekte (bei OctoMesh als CK-Typen):
  `EnergyCommunity`, `DailyEnergyPosition`, `PowerPlant`, `DailyMarketResult`,
  `EnergyPurchase`, `EnergySale`.
- **Konventionen:** IDs, Zeitstempel und Zeitzone; Energie in kWh, Preise in
  EUR/kWh; Status- und Fehlerwerte; Pflichtfelder und Validierung;
  Schema-Version und Beispieldaten.
- **Position je Gemeinschaft und Tag:** entweder Energieangebot **oder**
  Energiebedarf (kWh). Eine **Preisvorstellung ist optional** und nicht bindend;
  verbindliche Preislimits nur als gemeinsam abgestimmte Erweiterung. Einreichungsfrist
  und Marktschluss sind konfigurierbar; je Liefertag gibt es ein nachvollziehbares
  Marktergebnis.

Jede Plattform weist die **Konformität** mit einem automatisierten Test nach (M2).

## Aufgaben nach Meilenstein

| Bis | Aufgaben | Ihr liefert |
|---|---|---|
| Labor 1 bis 2 | Geschäftsmodell; Mengenlogik; **eigene, dokumentierte** Preis- und Zuteilungsregel | Fachkonzept |
| **M1** | gemeinsam mit den anderen IMC-Gruppen **Datenvertrag v1.0** (v0.1 Ende Okt.); erster Dienst über die Infra-Vorlage | Datenvertrag v1.0, Dienst läuft |
| **M2** | dokumentierte API eurer Plattform nach dem Datenvertrag: Position einreichen, ändern und stornieren bis zum Marktschluss, Request-ID für Idempotenz, Identität je Gemeinschaft; Konformitätstest | API-Dokumentation, Konformitätsprotokoll |
| **M3** | Liefertag frei wählbar (Marktkalender der Lehrenden); Marktschluss, Zuteilung nach eurer Regel, Kraftwerkseinsatz; Testmarkt mit mindestens zwei Gemeinschaften | Testmarkt-Protokoll |
| **M4** | Geschäfte und Marktergebnis nach Datenvertrag; Weboberfläche (Tagesergebnis, Handels- und Preisverlauf); die **neun Testszenarien** automatisiert; Handelsabrechnung (tatsächliche Ankauf- und Verkaufspreise je Gemeinschaft) | Web und API, Tests, Betriebsanleitung |

## Die neun Testszenarien

| Szenario | Erwartetes Verhalten |
|---|---|
| Ausgeglichener Markt | Nachfrage gedeckt, kein Kraftwerkseinsatz |
| Unterangebot | gesamtes Angebot der Gemeinschaften genutzt, Fehlmenge durch die Reserve gedeckt |
| Überangebot | nur die benötigte Menge angekauft, Zuteilung nach eurer dokumentierten Regel |
| Keine Nachfrage | kein Ankauf, keine Reserve, kein Verkaufspreis |
| Keine Angebote | die Reserve deckt im Standardfall die gesamte Nachfrage |
| Doppelter Request | keine doppelte Verarbeitung, kein doppelter Handelsabschluss |
| Parallele Einreichung | keine Überbuchung, konsistente Summen |
| Kraftwerksausfall | definierte Teilzuteilung oder nachvollziehbare Ablehnung |
| Korrektur nach Marktschluss | verändert keine bestätigten Handelsabschlüsse |

Geprüft werden Mengeninvarianten, Reproduzierbarkeit, Robustheit und
Datenvertragskonformität, **nicht** identische Preise oder Zuteilungen.

## Betrieb und Security

Pflicht: Container, Kubernetes-Deployment, dokumentierte API, Weboberfläche,
Health-Endpunkte und Observability in dash0. OctoMesh dürft ihr nutzen, es ist
aber kein Abnahmekriterium. Beachtet außerdem:

- Mandantengrenzen zwischen den Gemeinschaften, minimale Datenweitergabe
- Autorisierung je Aktion und Identität, Authentisierung und TLS
- Integrität und Audit der Abschlüsse; Replay- und Idempotenzschutz
- Least Privilege und sichere Secrets
- Zugriffe im Namen einer fremden Gemeinschaft werden abgewiesen,
  nachvollziehbar protokolliert und **nicht** als Handelsauftrag gespeichert

## Noch offen

- Wie die Gemeinschaften die drei Plattformen erreichen (alle drei gleichzeitig
  oder fest zugeordnet): wird bis Ende Labor 2 entschieden.
- Ob ein Matching von AIT in die Plattform integriert wird: wird mit den
  Lehrenden geklärt.

Vorlesungsbezug: Kapitel 2 B, 3 A, 3 C, 4 A bis C, 5 B.
