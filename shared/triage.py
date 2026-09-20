"""Triage scoring. EDUCATIONAL ONLY - not for real clinical use.

Priority levels: 1 = resuscitation ... 5 = non-urgent.
"""

# Keywords in the complaint that force at least this priority.
KEYWORD_MIN_PRIORITY = {
    "unconscious": 1,
    "not breathing": 1,
    "stroke": 2,
    "chest pain": 2,
    "bleeding": 3,
}


def vitals_priority(v):
    """Priority based on vital signs alone."""
    if v.spo2 < 90 or v.systolic_bp < 80 or v.heart_rate > 150 or v.heart_rate < 40 \
            or v.resp_rate > 30 or v.resp_rate < 8:
        return 1
    if v.spo2 < 94 or v.systolic_bp < 90 or v.heart_rate > 130 or v.resp_rate > 24 \
            or v.temp_c >= 40 or v.temp_c < 35:
        return 2
    if v.heart_rate > 110 or v.temp_c >= 38.5 or v.systolic_bp > 180 or v.resp_rate > 20:
        return 3
    if v.heart_rate > 100 or v.temp_c >= 37.8:
        return 4
    return 5


def assess(vitals, age, complaint=""):
    """Final priority: vitals, then keyword floor, then age adjustment."""
    level = vitals_priority(vitals)
    text = complaint.lower()
    for word, min_level in KEYWORD_MIN_PRIORITY.items():
        if word in text:
            level = min(level, min_level)
    if (age <= 1 or age >= 80) and level > 1:   # very young / very old: bump up
        level -= 1
    return level


def sort_queue(patients):
    """Most urgent first; ties go to whoever arrived first."""
    return sorted(patients, key=lambda p: (p.priority, p.created_at))
