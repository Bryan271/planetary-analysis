#!/usr/bin/env python3
"""Lightweight image sequencer/exporter for reviewing radar snapshots at variable speeds."""
import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List, Optional

try:
    import cv2  # type: ignore[import]
except ImportError as exc:  # pragma: no cover
    raise SystemExit("opencv-python is required. Install with `pip install opencv-python`." ) from exc

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')


def load_config(path: Path) -> List[dict]:
    with path.open('r', encoding='utf-8') as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError('Config must be a list of objects {"name", "path", "fps"?}.')
    return data


def collect_images(folder: Path, recursive: bool) -> List[Path]:
    if recursive:
        files = [p for p in folder.rglob('*') if p.suffix.lower() in SUPPORTED_EXTENSIONS]
    else:
        files = [p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS]
    return sorted(files)


def init_writer(target: Path, shape, fps: float) -> cv2.VideoWriter:
    target.parent.mkdir(parents=True, exist_ok=True)
    height, width = shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(target), fourcc, fps, (width, height))
    if not writer.isOpened():  # pragma: no cover
        raise RuntimeError(f'Unable to create video writer for {target}')
    return writer


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_') or 'sequence'


def play_sequence(
    images: List[Path],
    fps: float,
    scale: float,
    window_name: str,
    show: bool,
    export_path: Optional[Path],
) -> bool:
    if not images:
        print(f'[WARN] No images found for {window_name}.')
        return True
    delay_ms = max(1, int(1000 / fps))
    writer: Optional[cv2.VideoWriter] = None
    try:
        for img_path in images:
            frame = cv2.imread(str(img_path))
            if frame is None:
                print(f'[WARN] Could not read {img_path}')
                continue
            if scale != 1.0:
                frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            if export_path:
                if writer is None:
                    writer = init_writer(export_path, frame.shape, fps)
                if frame.ndim == 2:
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                writer.write(frame)
            if show:
                cv2.imshow(window_name, frame)
                key = cv2.waitKey(delay_ms)
                if key == 27:  # ESC
                    return False
    finally:
        if writer is not None:
            writer.release()
    return True


def auto_fps(image_count: int, target_duration: float, max_fps: float) -> float:
    if target_duration <= 0:
        return max_fps
    return min(max_fps, max(1.0, image_count / target_duration))


def run_playlist(entries: Iterable[dict], args: argparse.Namespace) -> None:
    for entry in entries:
        folder = Path(entry['path']).expanduser()
        name = entry.get('name', folder.name)
        fps = float(entry.get('fps', args.fps))
        images = collect_images(folder, args.recursive)
        if args.duration:
            fps = auto_fps(len(images), args.duration, args.fps)
        print(f'[INFO] Playing {name} @ {fps:.1f} fps ({folder})')
        export_path = None
        if args.export_dir:
            slug = slugify(name)
            export_path = args.export_dir / f'{slug}.mp4'
        if not play_sequence(images, fps, args.scale, f'image-player :: {name}', not args.no_display, export_path):
            break
        if not args.loop:
            continue


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Preview/export image directories at controllable speeds.')
    parser.add_argument('paths', nargs='*', help='Directories to play (optional if --config provided).')
    parser.add_argument('--config', type=Path, help='JSON playlist file (list of {"name","path","fps"}).')
    parser.add_argument('--fps', type=float, default=5.0, help='Default frames per second (default: 5).')
    parser.add_argument('--duration', type=float, help='Target seconds per dataset (overrides --fps).')
    parser.add_argument('--recursive', action='store_true', help='Traverse directories recursively.')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor applied to frames (default: 1.0).')
    parser.add_argument('--loop', action='store_true', help='Repeat forever until ESC is pressed.')
    parser.add_argument('--export-dir', type=Path, help='If set, write mp4 files for each dataset into this folder.')
    parser.add_argument('--no-display', action='store_true', help='Skip on-screen playback (for headless export).')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries: List[dict] = []
    if args.config:
        entries.extend(load_config(args.config))
    if args.paths:
        entries.extend({'path': p} for p in args.paths)
    if not entries:
        raise SystemExit('Provide --config and/or one or more directory paths.')
    if args.no_display and not args.export_dir:
        raise SystemExit('--no-display requires --export-dir to produce output.')
    try:
        run_playlist(entries, args)
    finally:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
