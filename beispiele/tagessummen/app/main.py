"""Tagessummen-Dienst: Beispiel für das Labor am 11.11.2026.

Liest die 15-Minuten-Werte einer Energiegemeinschaft über die GraphQL-API von OctoMesh
und liefert je Kalendertag die Summe pro Register. Ein Vorschlag als Startpunkt für die
Schnittstelle „Tagessummen/Tagesprofil“ an AIT, kein Vertrag.

Konfiguration nur über Umgebungsvariablen (im Cluster aus ConfigMap und Secret):

    OCTO_TENANT          Mandant, z. B. eg-lehrende
    OCTO_CLIENT_ID       Client-Credentials-Client mit Rolle StreamDataReader   (Secret)
    OCTO_CLIENT_SECRET   dessen Secret                                          (Secret)
    API_KEY              Schlüssel, den Aufrufer im Header X-API-Key mitschicken (Secret)
    OCTO_TOKEN_URL       Standard https://connect.machasing.com/connect/token
    OCTO_ASSETS_URL      Standard https://assets.machasing.com
    ARCHIVE_ID           Standard ec0000000000000000000a01 (15-Minuten-Werte)
    ZEITZONE             Standard Europe/Vienna; legt fest, wann ein Tag beginnt
"""
import datetime as dt
import logging
import os
import secrets
import socket
import time
from zoneinfo import ZoneInfo

import httpx
from fastapi import FastAPI, Header, HTTPException, Query, Response

VERSION = os.environ.get("APP_VERSION", "1.0")
POD = socket.gethostname()

TENANT = os.environ.get("OCTO_TENANT", "")
CLIENT_ID = os.environ.get("OCTO_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("OCTO_CLIENT_SECRET", "")
API_KEY = os.environ.get("API_KEY", "")
TOKEN_URL = os.environ.get("OCTO_TOKEN_URL", "https://connect.machasing.com/connect/token")
ASSETS_URL = os.environ.get("OCTO_ASSETS_URL", "https://assets.machasing.com").rstrip("/")
ARCHIVE_ID = os.environ.get("ARCHIVE_ID", "ec0000000000000000000a01")
ZEITZONE = ZoneInfo(os.environ.get("ZEITZONE", "Europe/Vienna"))
MAX_TAGE = 31

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tagessummen")

app = FastAPI(title="Tagessummen", version=VERSION)

# Das Token liegt nur im Arbeitsspeicher dieses Pods und wird nie ausgegeben.
_token = {"wert": "", "gueltig_bis": 0.0}


def token() -> str:
    if _token["wert"] and time.time() < _token["gueltig_bis"] - 60:
        return _token["wert"]
    r = httpx.post(TOKEN_URL, timeout=15, data={
        "grant_type": "client_credentials", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "scope": "octo_api", "acr_values": f"tenant:{TENANT}"})
    if r.status_code != 200:
        raise RuntimeError(f"Token-Abruf fehlgeschlagen: HTTP {r.status_code}")
    d = r.json()
    _token.update(wert=d["access_token"], gueltig_bis=time.time() + d.get("expires_in", 300))
    log.info("neues Token geholt, gültig %s s", d.get("expires_in"))
    return _token["wert"]


QUERY = """
query($a: OctoObjectId!, $from: DateTime, $to: DateTime) { streamData { transientStreamDataQuery {
  groupingAggregation(archiveRtId: $a, groupByColumnPaths: ["ObisCode"], columnPaths: [
    { attributePath: "Amount.Value", aggregationType: SUM },
    { attributePath: "Amount.Value", aggregationType: COUNT }],
    arg: { from: $from, to: $to, queryMode: DEFAULT }, first: 1) {
    items { rows(first: 100) { items { cells(first: 10) { items { attributePath value } } } } } } } } }
"""


def tagesgrenzen(tag: dt.date) -> tuple[dt.datetime, dt.datetime]:
    """Beginn und Ende eines Kalendertags in der eingestellten Zeitzone, als UTC."""
    # Übungsfehler: Das Image 1.1-fehler rechnet absichtlich in UTC-Tagen (für Rollback-Übung).
    zone = dt.timezone.utc if VERSION.endswith("-fehler") else ZEITZONE
    beginn = dt.datetime.combine(tag, dt.time(), zone)
    ende = dt.datetime.combine(tag + dt.timedelta(days=1), dt.time(), zone)
    return beginn.astimezone(dt.timezone.utc), ende.astimezone(dt.timezone.utc)


def summen_eines_tags(tag: dt.date) -> dict:
    von, bis = tagesgrenzen(tag)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    r = httpx.post(f"{ASSETS_URL}/tenants/{TENANT}/GraphQL", timeout=30,
                   headers={"Authorization": f"Bearer {token()}"},
                   json={"query": QUERY, "variables": {"a": ARCHIVE_ID, "from": von.strftime(fmt), "to": bis.strftime(fmt)}})
    r.raise_for_status()
    d = r.json()
    # GraphQL meldet Fehler mit HTTP 200 im Feld "errors".
    if d.get("errors"):
        raise RuntimeError("GraphQL: " + d["errors"][0].get("message", "unbekannter Fehler"))
    register = {}
    for item in d["data"]["streamData"]["transientStreamDataQuery"]["groupingAggregation"]["items"]:
        for row in item["rows"]["items"]:
            c = {x["attributePath"]: x["value"] for x in row["cells"]["items"]}
            register[c["ObisCode"]] = {"kwh": round(float(c["amountvalue_sum"] or 0), 3),
                                       "anzahl_werte": int(c["amountvalue_count"] or 0)}
    return {"datum": tag.isoformat(), "viertelstunden": int((bis - von).total_seconds() // 900), "register": register}


def pruefe_schluessel(x_api_key: str | None):
    if not API_KEY or not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="X-API-Key fehlt oder ist falsch")


@app.get("/tagessummen")
def tagessummen(response: Response,
                von: dt.date = Query(description="erster Tag, z. B. 2026-10-24"),
                bis: dt.date = Query(description="letzter Tag (inklusive)"),
                x_api_key: str | None = Header(default=None)):
    pruefe_schluessel(x_api_key)
    if bis < von or (bis - von).days >= MAX_TAGE:
        raise HTTPException(status_code=400, detail=f"Zeitraum: von <= bis, höchstens {MAX_TAGE} Tage")
    response.headers["X-Pod"] = POD
    try:
        tage = [summen_eines_tags(von + dt.timedelta(days=i)) for i in range((bis - von).days + 1)]
    except (httpx.HTTPError, RuntimeError) as e:
        log.error("OctoMesh-Abfrage fehlgeschlagen: %s", e)
        raise HTTPException(status_code=502, detail="OctoMesh nicht erreichbar oder Abfrage abgelehnt")
    log.info("tagessummen %s..%s, %d Tage", von, bis, len(tage))
    return {"mandant": TENANT, "zeitzone": str(ZEITZONE), "version": VERSION, "tage": tage}


@app.get("/healthz")
def healthz():
    """Liveness: Der Prozess antwortet."""
    return {"status": "ok", "pod": POD, "version": VERSION}


@app.get("/readyz")
def readyz():
    """Readiness: Konfiguration vollständig und ein Token von OctoMesh zu bekommen."""
    fehlt = [n for n, v in [("OCTO_TENANT", TENANT), ("OCTO_CLIENT_ID", CLIENT_ID),
                            ("OCTO_CLIENT_SECRET", CLIENT_SECRET), ("API_KEY", API_KEY)] if not v]
    if fehlt:
        raise HTTPException(status_code=503, detail="fehlt: " + ", ".join(fehlt))
    try:
        token()
    except (httpx.HTTPError, RuntimeError) as e:
        raise HTTPException(status_code=503, detail=str(e))
    return {"status": "bereit", "pod": POD}
