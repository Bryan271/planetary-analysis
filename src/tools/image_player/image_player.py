#!/usr/bin/env python3
"""Lightweight image sequencer for reviewing radar snapshots at variable speeds."""
import argparse
import json
import os
import time
from pathlib import Path
from typing import Iterable, List

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


def play_sequence(images: List[Path], fps: float, scale: float, window_name: str) -> bool:
    if not images:
        print(f'[WARN] No images found for {window_name}.')
        time.sleep(0.5)
        return True
    delay_ms = max(1, int(1000 / fps))
    for img_path in images:
        frame = cv2.imread(str(img_path))
        if frame is None:
            print(f'[WARN] Could not read {img_path}')
            continue
        if scale != 1.0:
            frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay_ms)
        if key == 27:  # ESC
            return False
    return True


def auto_fps(image_count: int, target_duration: float, max_fps: float) -> float:
    if target_duration <= 0:
        return max_fps
    return min(max_fps, max(1.0, image_count / target_duration))


def run_playlist(entries: Iterable[dict], args: argparse.Namespace) -> None:
    for entry in entries:
        folder = Path(entry['path']).expanduser()
        name = entry.get('name', folder.name)
        fps = entry.get('fps', args.fps)
        if args.duration:
            fps = auto_fps(len(list(folder.rglob('*'))) if args.recursive else len(list(folder.iterdir())), args.duration, args.fps)
        images = collect_images(folder, args.recursive)
        if args.duration:
            fps = auto_fps(len(images), args.duration, args.fps)
        print(f'[INFO] Playing {name} @ {fps:.1f} fps ({folder})')
        if not play_sequence(images, fps, args.scale, f'image-player :: {name}'):
            break
        if not args.loop:
            continue


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Preview image directories at controllable speeds.')
    parser.add_argument('paths', nargs='*', help='Directories to play (optional if --config provided).')
    parser.add_argument('--config', type=Path, help='JSON playlist file (list of {"name","path","fps"}).')
    parser.add_argument('--fps', type=float, default=5.0, help='Default frames per second (default: 5).')
    parser.add_argument('--duration', type=float, help='Target seconds per dataset (overrides --fps).')
    parser.add_argument('--recursive', action='store_true', help='Traverse directories recursively.')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor applied to frames (default: 1.0).')
    parser.add_argument('--loop', action='store_true', help='Repeat forever until ESC is pressed.')
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
    try:
        run_playlist(entries, args)
    finally:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
