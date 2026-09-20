import unittest

from shared.models import Vitals, Patient
from server.store import PatientStore

V = Vitals(80, 120, 16, 98, 36.8)


class StoreTests(unittest.TestCase):
    def test_version_increases_on_each_change(self):
        store = PatientStore()
        store.upsert(Patient("A", 30, "", V))
        store.upsert(Patient("B", 30, "", V))
        self.assertEqual(store.version, 2)

    def test_changes_since_returns_only_new_items(self):
        store = PatientStore()
        store.upsert(Patient("A", 30, "", V))
        store.upsert(Patient("B", 30, "", V))
        changed, version = store.changes_since(1)
        self.assertEqual([p.name for p in changed], ["B"])
        self.assertEqual(version, 2)


if __name__ == "__main__":
    unittest.main()
