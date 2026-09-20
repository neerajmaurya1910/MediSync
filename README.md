# MediSync

A Distributed Multi-device Triage Ecosystem.

> Educational project. The triage rules are simplified and **not for real clinical use**.

## How it works
Devices (bedside, nurse station, mobile) register patients with a central server.
The server scores each patient with shared triage logic and keeps a version counter.
Each device syncs by asking "what changed since version N?", and keeps a local cache
so it can still show the last known queue if the server is unreachable.

## Structure
- `shared/` - data models and triage scoring (used by server and clients)
- `server/` - central sync/coordination service (`app.py`, `store.py`)
- `client/` - device command-line client (`cli.py`)
- `tests/` - unit and API tests
- `docs/` - architecture, triage rules and the Sapling learning guide

## Run it (Python 3.9+, no installs needed)
```bash
python3 -m unittest discover -v        # run all tests
python3 -m server.app                  # terminal 1: start the server
python3 -m client.cli add --name "Asha" --age 34 --complaint "chest pain" \
    --hr 118 --bp 135 --rr 22 --spo2 95 --temp 37.2      # terminal 2
python3 -m client.cli queue
```

## Version Control
This project is managed with **Sapling SCM** (`sl`) and hosted on GitHub.
The workflow and commands used are documented in `docs/SAPLING_LEARNING.md`.
