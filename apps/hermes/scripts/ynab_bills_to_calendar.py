#!/usr/bin/env python3
"""Mirror upcoming YNAB scheduled outflows into the household Google Calendar.

Event IDs are a hash of (scheduled transaction id, date), so reruns update in
place. Only future events this script created are deleted when they no longer
match YNAB (e.g. amount/date changed). Past events are never touched.
"""
import calendar
import datetime as dt
import hashlib
import json
import os
import sys

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YNAB_URL = "https://wraeclast.bishop-bass.ts.net/ynab-mcp"
BUDGET_ID = "924a80ac-d251-40ed-96a3-a4a3d6f620d5"
KEY_FILE = "/opt/data/secrets/hermes-calendar.json"
WINDOW_DAYS = 45
TAG = "hermes-ynab-bills"


def add_months(d, n):
    m = d.month - 1 + n
    y, m = d.year + m // 12, m % 12 + 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


STEP = {
    "daily": lambda d, i, first: d + dt.timedelta(days=i),
    "weekly": lambda d, i, first: d + dt.timedelta(weeks=i),
    "everyOtherWeek": lambda d, i, first: d + dt.timedelta(weeks=2 * i),
    "every4Weeks": lambda d, i, first: d + dt.timedelta(weeks=4 * i),
    "monthly": lambda d, i, first: add_months(first, i),
    "everyOtherMonth": lambda d, i, first: add_months(first, 2 * i),
    "every3Months": lambda d, i, first: add_months(first, 3 * i),
    "every4Months": lambda d, i, first: add_months(first, 4 * i),
    "twiceAYear": lambda d, i, first: add_months(first, 6 * i),
    "yearly": lambda d, i, first: add_months(first, 12 * i),
    "everyOtherYear": lambda d, i, first: add_months(first, 24 * i),
}


def occurrences(st, start, end):
    first = dt.date.fromisoformat(st["date_next"])
    freq = st["frequency"]
    if freq == "never":
        return [first] if start <= first <= end else []
    if freq == "twiceAMonth":
        out, d = [], first
        for _ in range(40):
            if d > end:
                break
            if d >= start:
                out.append(d)
            d = d + dt.timedelta(days=15)
        return out
    step = STEP.get(freq)
    if not step:
        print(f"WARN unsupported frequency {freq} for {st['id']}", file=sys.stderr)
        return [first] if start <= first <= end else []
    out = []
    for i in range(0, 400):
        d = step(first, i, first)
        if d > end:
            break
        if d >= start:
            out.append(d)
    return out


def fetch_scheduled():
    h = {
        "Authorization": "Bearer " + os.environ["MCP_YNAB_MCP_API_KEY"],
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    def parse(r):
        r.raise_for_status()
        for line in r.text.splitlines():
            if line.startswith("data: "):
                return json.loads(line[6:])
        return r.json()

    r = requests.post(YNAB_URL, headers=h, timeout=30, json={
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "hermes", "version": "1.0"}}})
    parse(r)
    h["Mcp-Session-Id"] = r.headers["mcp-session-id"]
    requests.post(YNAB_URL, headers=h, timeout=30,
                  json={"jsonrpc": "2.0", "method": "notifications/initialized"})
    r = requests.post(YNAB_URL, headers=h, timeout=60, json={
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "list_scheduled_transactions",
                   "arguments": {"budget_id": BUDGET_ID}}})
    res = parse(r)["result"]["content"][0]["text"]
    return json.loads(res)


def title(st):
    payee = (st.get("payee_name") or "").replace("Transfer : ", "").strip()
    memo = (st.get("memo") or "").strip()
    label = payee
    if memo and memo.lower() not in payee.lower():
        label = f"{payee} - {memo}"
    return label


def main():
    today = dt.date.today()
    end = today + dt.timedelta(days=WINDOW_DAYS)
    want = {}
    for st in fetch_scheduled():
        if st.get("deleted") or st["amount"] >= 0:
            continue  # skip income and $0 placeholders
        for d in occurrences(st, today, end):
            eid = "hbill" + hashlib.sha1(f"{st['id']}:{d}".encode()).hexdigest()
            want[eid] = {
                "id": eid,
                "summary": title(st),
                "description": f"Account: {st.get('account_name')}\nCategory: {st.get('category_name')}\nSource: YNAB scheduled transaction (auto-synced by Hermes)",
                "start": {"date": d.isoformat()},
                "end": {"date": (d + dt.timedelta(days=1)).isoformat()},
                "extendedProperties": {"private": {"source": TAG}},
            }

    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE, scopes=["https://www.googleapis.com/auth/calendar"])
    svc = build("calendar", "v3", credentials=creds, cache_discovery=False)
    cid = os.environ["GOOGLE_CALENDAR_ID"]

    existing, tok = {}, None
    while True:
        resp = svc.events().list(
            calendarId=cid, privateExtendedProperty=f"source={TAG}",
            timeMin=f"{today}T00:00:00Z", maxResults=250, pageToken=tok,
            showDeleted=False, singleEvents=True).execute()
        for e in resp.get("items", []):
            existing[e["id"]] = e
        tok = resp.get("nextPageToken")
        if not tok:
            break

    created = updated = deleted = same = 0
    for eid, body in want.items():
        cur = existing.get(eid)
        if cur is None:
            try:
                svc.events().insert(calendarId=cid, body=body).execute()
                created += 1
            except HttpError as e:
                if e.resp.status == 409:  # id exists (e.g. cancelled earlier)
                    svc.events().update(calendarId=cid, eventId=eid,
                                        body={**body, "status": "confirmed"}).execute()
                    updated += 1
                else:
                    raise
        elif (cur.get("summary") != body["summary"]
              or cur["start"].get("date") != body["start"]["date"]):
            svc.events().update(calendarId=cid, eventId=eid, body=body).execute()
            updated += 1
        else:
            same += 1
    for eid, e in existing.items():
        start = e["start"].get("date") or e["start"].get("dateTime", "")[:10]
        if eid not in want and start >= today.isoformat():
            svc.events().delete(calendarId=cid, eventId=eid).execute()
            deleted += 1
    print(f"window {today}..{end}: created={created} updated={updated} "
          f"unchanged={same} deleted={deleted}")
    for eid, b in sorted(want.items(), key=lambda kv: kv[1]["start"]["date"]):
        print(b["start"]["date"], b["summary"])


if __name__ == "__main__":
    main()
