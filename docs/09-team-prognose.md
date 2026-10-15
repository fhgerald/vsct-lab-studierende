# 9 Team Prognose (AIT)

**Wer:** ein Team aus AIT, für alle Gemeinschaften.

## Ziel

Ein Dienst, der für **jede** Gemeinschaft aus historischen Tageswerten eine
nachvollziehbare **Prognose des Liefertags** erzeugt (Erzeugung, Verbrauch, Netto).
Ihr bewertet sie gegen das Ist und stellt sie über eine dokumentierte
Schnittstelle bereit. Ein einfaches, korrekt evaluiertes Modell genügt.

Die Gemeinschaften brauchen eure Prognose als Grundlage für ihre Tagesposition am
Markt. Nach den Kapitel-0-Folien liefert ihr Prognosen und aggregierte
Testprofile an die **Gemeinschaften**, nicht an die Handelsplattform.

## Wichtig: Daten nur bis D−2

Eine Position für den Liefertag D muss vor dem Marktschluss stehen. Der jüngste
eingefrorene Tag ist dann D−2. Eure Prognose für einen Tag D darf deshalb
**nur Daten bis D−2** verwenden, auch wenn bei historischen Marktläufen das Ist
längst vorliegt. So bleibt die Bewertung ehrlich.

## Aufgaben nach Meilenstein

| Bis | Aufgaben | Ihr liefert |
|---|---|---|
| Labor 1 bis 2 | Methode und Fehlermaß wählen (Baseline Vorwoche oder gleitender Mittelwert, saisonal, Regression, ML); mandantenübergreifenden Zugriff planen (ein Client je Gemeinschaft) | Methodenskizze |
| **M1** | Prototyp mit den Referenzdaten aus `eg-urstein` und `eg-lehrende` (befristeter Lesezugang), im Schema der Tagessummen; Dienst über die Infra-Vorlage | Prototyp läuft im Cluster |
| **M2** | **Vertrag der Prognose-Schnittstelle** (Gemeinschaft, Liefertag, Werte, Erstellungszeit, Modellversion); Anbindung an die Schnittstellen der ersten Gemeinschaften | Vertrag, erste echte Prognosen |
| **M3** | Prognose für alle Gemeinschaften; Vergleich mit dem Ist nach D+1; Fehlerkennzahl (MAE oder MAPE) je Gemeinschaft; Prognosen für die vorgegebenen historischen Liefertage nur mit Daten bis D−2 | Prognose-Schnittstelle, Evaluationsbericht |
| **M4** | Verbessertes Modell (Wetter und Rauschen, sobald die Simulation sie liefert) | Modellvergleich |

Der Lesezugang auf die Referenzgemeinschaften endet mit M2. Danach bekommt ihr die
Daten nur noch über die Schnittstellen der Gemeinschaften.

## Daten, die ihr nutzt

- Die **Tagessummen-Schnittstellen** der Gemeinschaften (Gemeinschaftssummen je
  Tag, bei Bedarf als 96-Slot-Profil). Keine Mitgliederdaten, keine einzelnen
  15-Minuten-Werte von Mitgliedern: Datenminimierung.
- Die Presets als Vergleichsprofile.
- Optional ein eigener OctoMesh-Mandant für die Ergebnisse, Pipeline-Endpunkte
  oder eine eigene API.
- dash0 für Beobachtbarkeit, der MCP-Server zum Erkunden.

## Noch offen

- Ob ein **Matching** (Lastprofil eines Interessenten → passende Gemeinschaft)
  zu eurer Aufgabe gehört: wird mit den Lehrenden geklärt. Bis dahin ist es
  Vertiefung.
- Wie genau die „aggregierten Testprofile“ aus den Folien aussehen und woher
  Wetterdaten kommen: wird mit den Lehrenden geklärt.

Vorlesungsbezug: Kapitel 1 B, 3 A und 3 C, 5 B, Gastvortrag CrateDB.
