# MediSync Architecture

```
 Bedside device ─┐
 Nurse station ──┼──  HTTP + JSON  ──►  Central server (server/app.py)
 Mobile device ──┘                        └─ PatientStore (version counter)
      │  local cache (.medisync_cache.json)
      └─ works offline, re-syncs later
```

## Sync protocol
1. Device stores `version` = last version it saw (starts at 0).
2. `GET /patients?since=<version>` returns only patients changed after that version,
   plus the server's current `version`.
3. Device merges them into its cache and saves the new version.

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| POST | `/patients` | Register a patient (server computes priority) |
| GET | `/patients?since=N` | Incremental sync |
| GET | `/queue` | Full queue, most urgent first |
| GET | `/health` | Liveness check |

## Ideas for later milestones
- Save data to SQLite instead of memory
- Edit/discharge a patient (updates bump the version too)
- Conflict handling when two devices edit the same patient
- Simple web dashboard for the nurse station
