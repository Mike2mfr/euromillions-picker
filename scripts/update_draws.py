#!/usr/bin/env python3
"""Append any new EuroMillions draws to draws.csv.

Downloads a public, validated EuroMillions results archive, checks every new
row, and appends only draws that are newer than the last line of draws.csv.
Existing history is never rewritten. Uses only the Python standard library.

Usage:  python scripts/update_draws.py
Exit codes: 0 = done (updated or already up to date), 1 = validation failed.
"""
import csv
import datetime as dt
import io
import json
import sys
import urllib.request
from pathlib import Path

SOURCE = "https://raw.githubusercontent.com/dev-baris/lottery-archive/main/eu/euromillions/results.csv"
ROOT = Path(__file__).resolve().parent.parent
DRAWS = ROOT / "draws.csv"
META = ROOT / "meta.json"
HEADER = ["date", "n1", "n2", "n3", "n4", "n5", "s1", "s2"]


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def validate(row):
    """Return a normalised row or raise ValueError."""
    date = dt.date.fromisoformat(row["date"])
    if date.weekday() not in (1, 4):  # Tuesday, Friday
        raise ValueError(f"{date} is not a Tuesday or Friday")
    main = sorted(int(row[k]) for k in HEADER[1:6])
    stars = sorted(int(row[k]) for k in HEADER[6:8])
    if len(set(main)) != 5 or not all(1 <= n <= 50 for n in main):
        raise ValueError(f"{date}: bad main numbers {main}")
    if len(set(stars)) != 2 or not all(1 <= s <= 12 for s in stars):
        raise ValueError(f"{date}: bad stars {stars}")
    return [date.isoformat(), *map(str, main), *map(str, stars)]


def main():
    local = list(csv.DictReader(DRAWS.open(newline="")))
    last_date = local[-1]["date"]
    known = {r["date"] for r in local}

    req = urllib.request.Request(SOURCE, headers={"User-Agent": "euromillions-picker"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    remote = list(csv.DictReader(io.StringIO(text)))
    if not remote or list(remote[0].keys())[:8] != HEADER:
        fail("source CSV has an unexpected format")

    # Safety check: the source must agree with our last 10 stored draws.
    remote_by_date = {r["date"]: r for r in remote}
    for r in local[-10:]:
        src = remote_by_date.get(r["date"])
        if src is None:
            continue
        if validate(src) != validate(r):
            fail(f"source disagrees with stored draw {r['date']}; not updating")

    new_rows = []
    for r in sorted(remote, key=lambda x: x["date"]):
        if r["date"] > last_date and r["date"] not in known:
            try:
                new_rows.append(validate(r))
            except ValueError as e:
                fail(str(e))

    if not new_rows:
        print(f"Already up to date (last draw {last_date}).")
        return

    with DRAWS.open("a", newline="") as f:
        if not DRAWS.read_text().endswith("\n"):
            f.write("\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerows(new_rows)

    meta = json.loads(META.read_text()) if META.exists() else {}
    meta["updated"] = dt.date.today().isoformat()
    meta["jackpot"] = ""  # unknown after an automatic update; the page hides it
    META.write_text(json.dumps(meta, ensure_ascii=False) + "\n")

    for r in new_rows:
        print(f"Added {r[0]}: {' '.join(r[1:6])}  stars {' '.join(r[6:8])}")


if __name__ == "__main__":
    main()
