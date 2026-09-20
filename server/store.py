"""In-memory patient store with a version counter, so devices can sync
by asking "what changed since version N?"."""
import threading

from shared.triage import sort_queue


class PatientStore:
    def __init__(self):
        self._patients = {}
        self._version = 0
        self._lock = threading.Lock()

    @property
    def version(self):
        return self._version

    def upsert(self, patient):
        with self._lock:
            self._version += 1
            patient.version = self._version
            self._patients[patient.id] = patient
            return patient

    def changes_since(self, version):
        with self._lock:
            changed = [p for p in self._patients.values() if p.version > version]
            return changed, self._version

    def queue(self):
        with self._lock:
            return sort_queue(self._patients.values())
