# Image Player

A sanitized utility for reviewing large image directories (e.g., radar frames) at adjustable playback speeds. It replaces the ad-hoc video player that lived alongside the original data dumps.

## Usage

```bash
pip install opencv-python
python src/tools/image_player/image_player.py /storage/path/to/frames --fps 8
```

Or drive multiple datasets via a JSON playlist:

```bash
python src/tools/image_player/image_player.py --config config/image_sets.example.json --duration 120
```

### Options
- `--fps` – default frames per second.
- `--duration` – target seconds per dataset (auto-computes fps from image count).
- `--recursive` – include images in subdirectories.
- `--scale` – resize frames (e.g., `0.5`).
- `--loop` – keep repeating until ESC is pressed.

## Config file format
`config/image_sets.example.json` shows the expected structure:

```json
[
  {"name": "example-aaa", "path": "/storage/.../example/aaa", "fps": 6},
  {"name": "example-bbb", "path": "/storage/.../example/bbb"}
]
```

Only sanitized placeholders are checked into Git; point the entries at your local `/storage` paths when you clone the repo.
