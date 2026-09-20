"""MediSync device client (bedside / nurse station), standard library only.

Examples (from the project root):
  python3 -m client.cli add --name "Asha" --age 34 --complaint "chest pain" \
      --hr 118 --bp 135 --rr 22 --spo2 95 --temp 37.2
  python3 -m client.cli queue
  python3 -m client.cli sync
"""
import argparse
import json
import os
import urllib.error
import urllib.request

from shared.models import Patient
from shared.triage import sort_queue

SERVER = os.environ.get("MEDISYNC_SERVER", "http://127.0.0.1:8080")
CACHE = os.environ.get("MEDISYNC_CACHE", ".medisync_cache.json")


def load_cache():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"version": 0, "patients": {}}


def save_cache(cache):
    with open(CACHE, "w") as f:
        json.dump(cache, f)


def request(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(SERVER + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.load(resp)


def sync(cache):
    """Fetch only what changed since our last version and merge it in."""
    result = request("GET", "/patients?since=%d" % cache["version"])
    for p in result["patients"]:
        cache["patients"][p["id"]] = p
    cache["version"] = result["version"]
    save_cache(cache)
    return len(result["patients"])


def print_queue(cache):
    patients = sort_queue(Patient.from_dict(p) for p in cache["patients"].values())
    if not patients:
        print("Queue is empty.")
    for p in patients:
        print("P%d  %-15s age %-3d %s" % (p.priority, p.name, p.age, p.complaint))


def main():
    parser = argparse.ArgumentParser(prog="medisync")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add", help="register a patient")
    add.add_argument("--name", required=True)
    add.add_argument("--age", type=int, required=True)
    add.add_argument("--complaint", default="")
    add.add_argument("--hr", type=int, required=True, help="heart rate")
    add.add_argument("--bp", type=int, required=True, help="systolic BP")
    add.add_argument("--rr", type=int, required=True, help="respiratory rate")
    add.add_argument("--spo2", type=int, required=True)
    add.add_argument("--temp", type=float, required=True, help="Celsius")
    sub.add_parser("queue", help="show the triage queue")
    sub.add_parser("sync", help="sync this device with the server")
    args = parser.parse_args()

    cache = load_cache()
    try:
        if args.cmd == "add":
            created = request("POST", "/patients", {
                "name": args.name, "age": args.age, "complaint": args.complaint,
                "vitals": {"heart_rate": args.hr, "systolic_bp": args.bp,
                           "resp_rate": args.rr, "spo2": args.spo2,
                           "temp_c": args.temp}})
            print("Added %s -> priority %d" % (created["name"], created["priority"]))
        else:
            print("Synced %d change(s)." % sync(cache))
            if args.cmd == "queue":
                print_queue(cache)
    except (urllib.error.URLError, OSError):
        if args.cmd == "add":
            print("Server unreachable - patient NOT saved.")
        else:
            print("Server unreachable - showing last synced data.")
            print_queue(cache)


if __name__ == "__main__":
    main()
