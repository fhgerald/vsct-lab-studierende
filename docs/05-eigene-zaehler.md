# 5 Eigene Zähler melden

Ab **Labor 4b (~04.12.)** könnt ihr in eurer Gemeinschaft eigene Zähler anlegen
und Viertelstundenwerte melden, zum Beispiel einen Speicher als zwei Zähler
(Laden = Verbrauch, Entladen = Erzeugung). Die Wirkung seht ihr nach der
Verteilung D+1 im Deckungsgrad. Bis dahin sind die Endpunkte für Gruppen nicht
freigeschaltet.

Ihr braucht dafür von der Betreuung einen **Client** mit der Rolle `MeterReporter`
und die Token-Adresse. Das Client-Secret ist wie ein Passwort zu behandeln
([Seite 2](02-zugang.md)).

## Die drei Routen

Alle Aufrufe sind `POST` mit `Authorization: Bearer <token>` und JSON-Body auf

```
https://adapter-<tenant>.machasing.com/<tenant>/<route>
```

| Route | Wofür |
|---|---|
| `/registerMeteringPoint` | Zählpunkt anlegen (wiederholbar) |
| `/meterReadings` | Viertelstundenwerte melden, bis zum Meldeschluss |
| `/communityBalance` | vorläufige Bilanz lesen, schreibt nichts |

## 1. Token holen

Flow `client_credentials`. Zwei Parameter sind Pflicht, sonst gibt es **HTTP 401**,
auch wenn Rolle und Tenant stimmen:

- `scope=octo_api`
- `acr_values=tenant:<tenant>`

Dazu `grant_type=client_credentials`, `client_id` und `client_secret` eures Clients,
als Formular (`application/x-www-form-urlencoded`) an die Token-URL. Das Secret
gehört nie in ein Repository oder einen Chat.

## 2. Zählpunkt anlegen

`/registerMeteringPoint`. Die Nummer hat genau **33 Zeichen** und liegt im
reservierten Bereich `AT009998…`. `direction` ist `consumption` oder `production`.

```json
{ "meteringPointNumber": "AT0099980000000000000000000000081",
  "direction": "consumption",
  "displayName": "Gruppe 1" }
```

Ein zweiter Aufruf mit gleicher Nummer und Richtung legt nichts neu an
(`created: false`). Weitere Felder wie `participationFrom` (Datum) und
`participationFactor` (Prozent, z. B. 100) kennt der Endpunkt ebenfalls.

## 3. Werte senden

`/meterReadings`. Die Grenzen liegen im 15-Minuten-Raster, UTC, ein Wert (`kWh`)
pro Slot. Mehrere Zählpunkte und Slots pro Aufruf sind möglich.

```json
{ "readings": [
  { "meteringPointNumber": "AT0099980000000000000000000000081",
    "direction": "consumption",
    "values": [ { "from": "2026-10-16T08:00:00Z", "to": "2026-10-16T08:15:00Z", "kWh": 0.8 } ] } ] }
```

**Meldeschluss:** Werte für einen Tag nimmt der Endpunkt nur bis D+1 06:00 (Wien)
an. Danach lehnt er den Tag mit `DAY_FROZEN` ab; `frozenUntil` in der Antwort
nennt die Grenze. Werte für „gestern“ nach dem Meldeschluss werden abgelehnt.

**Das Ergebnis steht im Feld `status`** (`ok`, `partial`, `error`), nicht im
HTTP-Code. Die Endpunkte antworten auch bei Teilfehlern mit 200.

## 4. Bilanz lesen

`/communityBalance`:

```json
{ "slots": 4 }
```

Die Antwort ist **vorläufig** und wird am Folgetag vom endgültigen Lauf abgelöst.
Sie hinkt dem Schreiben **etwa eine Minute** hinterher: Wer sofort nach dem Senden
fragt, sieht die neuen Werte noch nicht. Man kann auf bestimmte Zählpunkte
einschränken:

```json
{ "slots": 4, "meteringPoints": [ "AT0099980000000000000000000000081" ] }
```

Beispiel pro Viertelstunde: 1,2 kWh Erzeugung, 0,8 kWh Verbrauch ergeben
0,4 kWh Überschuss.

## Wer darf was

| Aufruf | Ergebnis |
|---|---|
| ohne Token | 401 |
| Token ohne die passende Rolle für die Route | 403 |
| Client einer anderen Gemeinschaft | 403 |
| Rolle `MeterReporter` auf die drei Routen oben | 200 |

Auf andere Routen, zum Beispiel für manuelle Korrekturen einzelner Werte, hat die Rolle `MeterReporter` keinen Zugriff.

Weiterführend: Tutorial
[Pipeline endpoints](https://docs.meshmakers.cloud/docs/tutorials/pipelineEndpoints).
