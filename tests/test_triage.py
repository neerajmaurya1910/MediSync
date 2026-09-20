import unittest

from shared.models import Vitals, Patient
from shared.triage import assess, sort_queue

NORMAL = Vitals(heart_rate=80, systolic_bp=120, resp_rate=16, spo2=98, temp_c=36.8)


class TriageTests(unittest.TestCase):
    def test_normal_vitals_are_lowest_priority(self):
        self.assertEqual(assess(NORMAL, age=30), 5)

    def test_low_oxygen_is_critical(self):
        v = Vitals(80, 120, 16, 85, 36.8)
        self.assertEqual(assess(v, age=30), 1)

    def test_chest_pain_raises_priority(self):
        self.assertEqual(assess(NORMAL, age=30, complaint="Chest pain"), 2)

    def test_elderly_are_bumped_up(self):
        v = Vitals(105, 120, 16, 98, 36.8)   # priority 4 on vitals alone
        self.assertEqual(assess(v, age=85), 3)

    def test_queue_orders_by_priority_then_arrival(self):
        a = Patient("A", 30, "", NORMAL, priority=3, created_at=2.0)
        b = Patient("B", 30, "", NORMAL, priority=1, created_at=3.0)
        c = Patient("C", 30, "", NORMAL, priority=3, created_at=1.0)
        self.assertEqual([p.name for p in sort_queue([a, b, c])], ["B", "C", "A"])


if __name__ == "__main__":
    unittest.main()
