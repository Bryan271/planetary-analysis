# 24AUG23 Functional Vector Prototype

## Purpose
This build is the first public-friendly snapshot of the "functional vector analysis" concept: an automation harness that sweeps radar layers, records the imagery, and replays it at variable speeds to surface subtle motion cues. It is intentionally minimal—designed to prove that the capture/inspection loop works end-to-end (automation ➜ data ➜ review) before the full analytical stack was ready.

## What it demonstrates
- **Radar ingestion pipeline:** the Tkinter/Selenium prototype drives the NOAA/Ventusky endpoints, saves frames to the SATA dataset, and can run unattended for hours.
- **Hot-reload friendly code:** the Python modules are small, letting us patch `selenium_module.py` or tweak schedulers in real time while the job is running.
- **Human-in-the-loop playback:** the new image player replaces the private tooling so we can scrub any dataset (`aaa`–`eee`) at controlled speeds and compare patterns live.
- **Data curation:** manifests keep the multi-GB image sets off GitHub while still documenting where every part lives (`storage/projects/planetary-analysis/raw/...`).

## Known limitations
- One monolithic GUI thread (no async/error isolation).
- Hard-coded URLs/credentials; config system still TODO.
- Logging is rudimentary (stdout + flat files).
- No analytical transforms yet—just capture + playback.

## Next steps
1. Package the code (type hints, dependency injection, config files).
2. Introduce task runners for parallel site capture and resilience.
3. Layer in the functional vector analysis modules (signal extraction, statistical windows, alerting).
4. Publish sanitized sample outputs + notebooks once the analytical core lands.

Reference files:
- Source: `src/prototype/24aug23_new_code/`
- Data: `/storage/projects/planetary-analysis/raw/24AUG23_New_Code_extracted/24AUG23_New_Code/`
- Image player: `src/tools/image_player/`
