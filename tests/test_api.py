import json
import threading
import unittest
import urllib.error
import urllib.request

from server.app import make_server
from server.store import PatientStore

GOOD = {"name": "Asha", "age": 34, "complaint": "chest pain",
        "vitals": {"heart_rate": 118, "systolic_bp": 135, "resp_rate": 22,
                   "spo2": 95, "temp_c": 37.2}}


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.server = make_server(PatientStore(), port=0, quiet=True)
        self.base = "http://127.0.0.1:%d" % self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def post(self, body):
        req = urllib.request.Request(self.base + "/patients",
                                     data=json.dumps(body).encode(), method="POST")
        return urllib.request.urlopen(req)

    def test_add_then_sync(self):
        self.assertEqual(self.post(GOOD).status, 201)
        with urllib.request.urlopen(self.base + "/patients?since=0") as r:
            data = json.load(r)
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["patients"][0]["priority"], 2)

    def test_bad_data_is_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post({"name": "No vitals"})
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
