# 24AUG23 Prototype Source

Recovered from the `24AUG23_New_Code` archive delivered via `Full_split_upload`. The original assets live on the SATA volume at:

```
/storage/projects/planetary-analysis/raw/24AUG23_New_Code_extracted/24AUG23_New_Code/24AUG23 New Code/
```

Large radar folders (`aaa`–`eee`) remain on the SATA disk (tens of GB each) and are not committed to Git. This folder captures the Python sources that drive the vector-mapping prototype:

- `main.py` – Tk entry point
- `gui_module.py` – operator UI + Selenium handler wiring
- `scheduler.py` – interval helper
- `selenium_module.py` & `selenium_module_old.py` – automation logic
- `logger.py` – simple stdout/file logger

Next steps:
1. Refactor this code into a package (type hints, config, tests).
2. Wire it to the new datasets without blocking the UI thread.
3. Keep raw data under `/storage` and track it via manifests.
