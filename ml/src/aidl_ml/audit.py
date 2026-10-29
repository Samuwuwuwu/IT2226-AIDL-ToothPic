"""Count image files in class-labelled subfolders (not a quality/leakage audit)."""

from __future__ import annotations

import argparse
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def count_images(root: Path) -> dict[str, int]:
    """Count supported image extensions below each immediate class directory."""
    if not root.is_dir():
        raise ValueError(f"Dataset directory does not exist: {root}")
    folders = sorted((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.name)
    if not folders:
        raise ValueError(f"No class subdirectories in: {root}")
    return {
        folder.name: sum(
            1 for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
        )
        for folder in folders
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_root", type=Path)
    args = parser.parse_args()
    try:
        counts = count_images(args.dataset_root)
    except ValueError as exc:
        parser.error(str(exc))
    for label, count in counts.items():
        print(f"{label:<30} {count:>6}")
    print(f"{'TOTAL':<30} {sum(counts.values()):>6}")
    print("Counts only; verify duplicate images, file integrity and label quality separately.")


if __name__ == "__main__":
    main()
