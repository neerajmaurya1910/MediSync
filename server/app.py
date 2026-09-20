"""Central MediSync server (standard library only).

Run from the project root:  python3 -m server.app
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from shared.models import Patient, Vitals
from shared.triage import assess
from server.store import PatientStore


def build_patient(data):
    """Validate the incoming JSON and build a Patient with a computed priority."""
    try:
        vitals = Vitals(
            heart_rate=int(data["vitals"]["heart_rate"]),
            systolic_bp=int(data["vitals"]["systolic_bp"]),
            resp_rate=int(data["vitals"]["resp_rate"]),
            spo2=int(data["vitals"]["spo2"]),
            temp_c=float(data["vitals"]["temp_c"]),
        )
        patient = Patient(name=str(data["name"]), age=int(data["age"]),
                          complaint=str(data.get("complaint", "")), vitals=vitals)
    except (KeyError, TypeError, ValueError) as err:
        raise ValueError("bad patient data: %s" % err)
    patient.priority = assess(vitals, patient.age, patient.complaint)
    return patient


def make_server(store, host="127.0.0.1", port=8080, quiet=False):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            if not quiet:
                super().log_message(fmt, *args)

        def _send(self, code, payload):
            body = json.dumps(payload).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/health":
                self._send(200, {"status": "ok"})
            elif url.path == "/patients":
                try:
                    since = int(parse_qs(url.query).get("since", ["0"])[0])
                except ValueError:
                    return self._send(400, {"error": "since must be a number"})
                changed, version = store.changes_since(since)
                self._send(200, {"version": version,
                                 "patients": [p.to_dict() for p in changed]})
            elif url.path == "/queue":
                self._send(200, {"queue": [p.to_dict() for p in store.queue()]})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            if urlparse(self.path).path != "/patients":
                return self._send(404, {"error": "not found"})
            try:
                length = int(self.headers.get("Content-Length", 0))
                patient = build_patient(json.loads(self.rfile.read(length)))
            except (ValueError, json.JSONDecodeError) as err:
                return self._send(400, {"error": str(err)})
            self._send(201, store.upsert(patient).to_dict())

    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    server = make_server(PatientStore())
    print("MediSync server running on http://127.0.0.1:8080  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
