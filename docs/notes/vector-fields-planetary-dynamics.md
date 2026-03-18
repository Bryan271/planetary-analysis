# Vector Fields of Planetary Dynamics

A running log of the design discussions that tie the automation stack to the underlying planetary math.

## 1. Introduction
- Objective: fuse disparate planetary datasets into a cohesive narrative.
- Emphasis on marrying theoretical physics (declination, axial tilt) with practical visualization.

## 2. Program analysis
- Preserve the legacy prototype, build a cleaner app for the expanded scope.
- Module boundaries:
  - `main.py` – entry point.
  - `gui_module.py` – operator controls.
  - `selenium_module.py` – collection + automation.
  - `logger.py` – telemetry + debugging.

## 3. Structure & math
- Need a tighter GUI with support for multiple URLs/parameter sweeps.
- Derived and validated the solar-declination formula to keep Earth views aligned.
- Tested the math against multiple days-of-year, discussed geometric implications.

## 4. Technical considerations
- Window-specific captures + potential parallel sessions.
- Automation aides: Windows Task Scheduler, dedicated hotkeys.
- Tooling/technology scouting for scalability and richer analysis.

## 5. Strategic planning
- Build/run checklist before automating captures.
- Maintain clear milestone summaries and a forward-looking roadmap.

## 6. Documentation & record keeping
- Keep detailed engineering notes.
- Declination formula (same as in the dedicated math note) anchors the address-bar parameters.
