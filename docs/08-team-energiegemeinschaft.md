# 8 Team Energiegemeinschaft

**Wer:** je Kleingruppe ein Team aus CYS und IIR. Jedes Team betreibt **eine
eigene Gemeinschaft** (Mandant `eg-<team>`).

## Ziel

Ihr betreibt eure Gemeinschaft als eigene Domäne: Stammdaten, Datenpipeline,
Simulation und eigene Zähler, Abrechnung der Mitglieder, Security. Eure Daten
stellt ihr dem Prognose-Team über eine vereinbarte Schnittstelle bereit. Am
Markt handelt ihr eine **Tagesposition**. Rollen im Team: Community Management
und Abrechnung, Datenpipeline und Simulation (IIR), Security (CYS).

## Was ihr vorfindet

Euer Mandant mit einem Preset, zwei Jahren Daten, täglicher Simulation und
Verteilung D+1 ([Seite 4](04-daten-und-simulation.md)). Eure Schnittstellen nach
außen folgen den Verträgen; wie ihr sie baut (OctoMesh-Pipelines oder ein eigener
Dienst), ist euch freigestellt, solange Authentisierung und Rollen stimmen.

## Aufgaben nach Meilenstein

| Bis | Aufgaben | Ihr liefert |
|---|---|---|
| Labor 1 bis 2 | Fachmodell (Kunde, Anlage, Zählpunkt, Teilnahmefaktor, Preis); Bedrohungsmodell und Datenklassifikation (15-Minuten-Lastgänge sind personenbezogen) | Fachmodell, Bedrohungsmodell v1 |
| **M1** | Rollenkonzept im Mandanten (Personen, Dienste, Clients) mit dem Security-Board; erster Dienst über die Infra-Vorlage | Rollenkonzept, Dienst läuft |
| Labor 3 bis **M2** | Daten des eigenen Presets verstehen (Deckungsgrad D, Überschussquote U); eigene Stammdaten ergänzen ([Seite 6](06-stammdaten-import.md)); **Schnittstelle „Tagessummen/Tagesprofil“** für AIT, rollengeschützt, mit einem Client für AIT | Schnittstelle mit Vertrag, Freigabeprotokoll |
| Labor 4a | Tagesbilanz aus der Verteilung D+1 ableiten ([Seite 1](01-ueberblick.md)) | Tagesbilanz-Dienst |
| Labor 4b | Eigene Zähler anmelden und melden, z. B. einen Speicher als zwei Zähler ([Seite 5](05-eigene-zaehler.md)) | Wirkung in der Verteilung D+1 sichtbar |
| **M3** | Grundabrechnung der Mitglieder aus `G.03` bzw. `G.01T − P.01T` (nur Qualität L1/L2); Tagesposition aus der AIT-Prognose an die Handelsplattform (Testmarkt); Zugriffsmatrix testen (fremdes Token wird abgelehnt) | Abrechnung auf echten Daten, Position im Testmarkt, Testprotokoll |
| **M4** | Marktgeschäfte (Ankauf, Verkauf laut Datenvertrag) in die Mitgliederabrechnung übernehmen (Erlös an Erzeuger, Kosten an Verbraucher; Regel dokumentieren); Abweichung Position gegen Ist auswerten; Security-Audit einer fremden Gemeinschaft (Auftrag kommt von den Lehrenden); Randfälle (Tag ohne Erzeugung, nachgemeldete Werte, `L3`-Daten) | Abrechnung mit Markt, Auswertung, Auditbericht |

## Daten, die ihr nutzt

- GraphQL auf eure Runtime-Entitäten ([Seite 4](04-daten-und-simulation.md)),
  Stream-Data-Archive `ec…a01` (15 Minuten) und die Rollups `ec…a02` bis `a06`.
- Register `1-1:1.9.0 G.01`, `1-1:2.9.0 G.01`, `G.03`, `G.01T`, `P.01T`
  ([Seite 3](03-energiegemeinschaft-fachlich.md)).
- Einstellungen und Reset-Aufträge der Simulation.
- Die Produkt-Abrechnung und die App sind nur Referenz in `eg-urstein`; in eurem
  Mandanten ist die Produkt-Abrechnung nicht installiert. **Ihr baut eure eigene.**
- Der MCP-Server (`https://mcp.machasing.com/mcp`) zum Erkunden mit KI-Clients,
  siehe Tutorial
  [AI via the MCP server](https://docs.meshmakers.cloud/docs/tutorials/aiWithMcp).

## Security: worauf ihr achten sollt

Die konkreten Prüfaufträge bekommt ihr im Labor. Denkt schon jetzt an diese Punkte:

1. Die Mandantengrenze hält. Das soll nachgewiesen werden.
2. Innerhalb eines Mandanten ist die generische Abfrageschnittstelle grob.
   Feingranulare Rechte entstehen erst über kuratierte Schnittstellen mit
   Pflichtrollen.
3. Unterscheidet, wo eine Berechtigung **angezeigt** und wo sie **durchgesetzt**
   wird (Oberfläche oder API).
4. Zwischen Namespaces gibt es nicht automatisch eine Netzwerkgrenze.
5. Dienst-Identitäten brauchen Pflichtrollen und eine Bindung an den Mandanten.

Vorlesungsbezug: Kapitel 2 A und B, 3 B und C, 4, 5 B.
