# 11 Fallen und Hilfe

Dinge, die erfahrungsgemäß Zeit kosten.

## Abfragen und Daten

- **GraphQL-Fehler kommen mit HTTP 200.** Immer das Feld `errors` in der Antwort
  prüfen. In Protokollen taucht dazu nichts auf.
- **Attribute immer explizit anfordern.** Wer bei generischen Abfragen
  (`runtimeEntities`) `attributeNames` weglässt, bekommt alle Attribute.
- **Zeitzonen.** Archive speichern UTC. Ein Tag der Gemeinschaft beginnt um
  Mitternacht Wien (`22:00Z` im Sommer, `23:00Z` im Winter).
- **15-Minuten-Raster.** Abfragen und Meldungen immer auf `:00`, `:15`, `:30`,
  `:45` legen.
- **Der laufende Tag hat noch keine Verteilung.** Sie kommt erst am Folgetag; der
  Vortag wird nach dem Meldeschluss eingefroren.

## Eigene Zähler und Endpunkte

- **Token ohne `scope=octo_api` oder ohne `acr_values=tenant:<tenant>` ergibt 401**,
  auch wenn Rolle und Tenant stimmen.
- **Meldeschluss.** Werte für einen Tag nimmt der Endpunkt nur bis D+1 06:00
  (Wien) an; danach `DAY_FROZEN`.
- **HTTP-Endpunkte antworten mit 200.** Das Ergebnis steht im Feld `status`
  (`ok`, `partial`, `error`).
- **Die Bilanz hinkt etwa eine Minute hinterher.** Nach dem Melden kurz warten.

## Kubernetes

- **Quota.** Ein Pod ohne `resources.limits` scheitert mit
  `pods forbidden: failed quota`.
- **Zugang.** Die Kubernetes-API ist nur über FH-VPN oder eduroam erreichbar.

## Sicherheit

- `octo-cli -c AuthStatus` und `~/.octo-cli/contexts.json` enthalten euer Token.
  Nie kopieren, nie in einen Chat oder eine KI-Unterhaltung.
- Client-Secrets nie in ein Repository.

## Hilfe

- Fragen zu Zugang, Passwort, Reset: Betreuung im Labor oder in FH-Teams.
- Fragen zur Plattform: zuerst die Tutorials und die OctoMesh-Dokumentation
  (<https://docs.meshmakers.cloud>), dann die Betreuung.
- Störungen (Seite nicht erreichbar, Daten fehlen): mit Uhrzeit, Mandant und
  Fehlermeldung an die Betreuung, **ohne** Token oder Passwort.

## Tutorials

Die allgemeinen Tutorials sind auf Englisch online. Sie verwenden Platzhalter
statt der Labor-Adressen: ersetzt `<your-domain>` durch `machasing.com` und
`<tenant>` durch eure Gemeinschaft.

| Tutorial | Wofür |
|---|---|
| [Getting started](https://docs.meshmakers.cloud/docs/tutorials/gettingStarted) | Begriffe, Studio-Rundgang, octo-cli |
| [Accessing data](https://docs.meshmakers.cloud/docs/tutorials/accessingData) | Token, GraphQL, Zeitreihen, Python-Beispiel |
| [Understanding energy data](https://docs.meshmakers.cloud/docs/tutorials/energyData) | Modell, Register, Verteilung, Kennzahlen |
| [Pipeline endpoints](https://docs.meshmakers.cloud/docs/tutorials/pipelineEndpoints) | eigene Zähler melden, Schnittstellen bauen |
| [AI via the MCP server](https://docs.meshmakers.cloud/docs/tutorials/aiWithMcp) | KI-Client anbinden, erkunden, Prototyp bauen |
