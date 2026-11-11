"""Compare raw class folders by image color, dimensions, and embedded metadata."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from PIL import ExifTags, Image, ImageDraw, ImageStat

ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
FEATURES = (
    "mean_r",
    "mean_g",
    "mean_b",
    "brightness",
    "brightness_std",
    "saturation",
    "width",
    "height",
    "aspect_ratio",
    "file_kb",
)
CATEGORIES = (
    "extension", "format", "mode", "icc_profile", "exif_make", "exif_model", "exif_software"
)
COLORS = (
    (50, 110, 180), (225, 100, 70), (70, 155, 100),
    (160, 100, 180), (220, 165, 45), (70, 165, 175),
)


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def exif_text(image: Image.Image, wanted: str) -> str:
    try:
        for tag, value in image.getexif().items():
            if ExifTags.TAGS.get(tag) == wanted:
                if isinstance(value, bytes):
                    value = value.decode("utf-8", errors="replace")
                return str(value).strip()
    except Exception:
        pass
    return ""


def profile(path: Path, dataset: Path, label: str) -> dict[str, object]:
    with Image.open(path) as image:
        width, height = image.size
        record: dict[str, object] = {
            "class": label,
            "image": path.relative_to(dataset).as_posix(),
            "extension": path.suffix.lower(),
            "format": image.format or "",
            "mode": image.mode,
            "width": width,
            "height": height,
            "aspect_ratio": width / height if height else 0,
            "file_kb": path.stat().st_size / 1024,
            "icc_profile": "yes" if image.info.get("icc_profile") else "no",
            "exif_make": exif_text(image, "Make"),
            "exif_model": exif_text(image, "Model"),
            "exif_software": exif_text(image, "Software"),
        }

        sample = image.convert("RGB")
        sample.thumbnail((128, 128))
        rgb_stats = ImageStat.Stat(sample)
        gray_stats = ImageStat.Stat(sample.convert("L"))
        hsv_stats = ImageStat.Stat(sample.convert("HSV"))
        record.update(
            mean_r=rgb_stats.mean[0],
            mean_g=rgb_stats.mean[1],
            mean_b=rgb_stats.mean[2],
            brightness=gray_stats.mean[0],
            brightness_std=gray_stats.stddev[0],
            saturation=hsv_stats.mean[1],
        )
        return record


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def draw_profiles(path: Path, groups: dict[str, list[dict[str, object]]]) -> None:
    panel_w, panel_h, columns = 410, 290, 3
    rows = (len(FEATURES) + columns - 1) // columns
    canvas = Image.new("RGB", (panel_w * columns, panel_h * rows), "white")
    draw = ImageDraw.Draw(canvas)
    classes = sorted(groups)

    for index, feature in enumerate(FEATURES):
        left = (index % columns) * panel_w
        top = (index // columns) * panel_h
        draw.text((left + 8, top + 8), feature.replace("_", " ").title(), fill="black")
        summaries = {
            label: [float(row[feature]) for row in records]
            for label, records in groups.items()
        }
        endpoints = [
            percentile(values, quantile)
            for values in summaries.values()
            for quantile in (0.05, 0.95)
        ]
        low, high = min(endpoints), max(endpoints)
        if high == low:
            high = low + 1
        chart_left, chart_right = left + 145, left + panel_w - 12
        chart_w = chart_right - chart_left
        row_h = 27
        y_start = top + 42
        for class_index, label in enumerate(classes):
            values = summaries[label]
            q05, q25, median, q75, q95 = [
                percentile(values, q) for q in (0.05, 0.25, 0.5, 0.75, 0.95)
            ]
            y = y_start + class_index * row_h

            def x(value: float) -> int:
                return chart_left + round((value - low) / (high - low) * chart_w)

            color = COLORS[class_index % len(COLORS)]
            draw.text((left + 8, y - 7), label[:21], fill="black")
            draw.line((x(q05), y, x(q95), y), fill="#555555", width=2)
            draw.line((x(q05), y - 5, x(q05), y + 5), fill="#555555", width=2)
            draw.line((x(q95), y - 5, x(q95), y + 5), fill="#555555", width=2)
            draw.rectangle((x(q25), y - 7, x(q75), y + 7), fill=color, outline="#222222")
            draw.line((x(median), y - 8, x(median), y + 8), fill="black", width=2)

        axis_y = y_start + len(classes) * row_h + 4
        draw.line((chart_left, axis_y, chart_right, axis_y), fill="#888888")
        draw.text((chart_left, axis_y + 4), f"{low:.2f}", fill="#444444")
        draw.text((chart_right - 48, axis_y + 4), f"{high:.2f}", fill="#444444")

    canvas.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=ROOT / "data" / "raw" / "school_oral")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "profile_report")
    args = parser.parse_args()
    dataset = args.dataset.resolve()
    if not dataset.is_dir():
        parser.error(f"Dataset folder not found: {dataset}")
    class_folders = sorted(path for path in dataset.iterdir() if path.is_dir())
    if not class_folders:
        parser.error(f"No class folders found in: {dataset}")

    records: list[dict[str, object]] = []
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    metadata: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    skipped = 0
    for folder in class_folders:
        for path in folder.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            try:
                row = profile(path, dataset, folder.name)
            except Exception:
                skipped += 1
                continue
            records.append(row)
            groups[folder.name].append(row)
            for category in CATEGORIES:
                value = str(row[category]) or "<missing>"
                metadata[(folder.name, category)][value] += 1

    if not records:
        parser.error("No readable images found in the class folders.")
    args.output.mkdir(parents=True, exist_ok=True)
    image_fields = ["class", "image", *FEATURES, *CATEGORIES]
    write_csv(args.output / "image_profiles.csv", records, image_fields)

    summary: list[dict[str, object]] = []
    for label, items in sorted(groups.items()):
        row: dict[str, object] = {"class": label, "image_count": len(items)}
        for feature in FEATURES:
            values = [float(item[feature]) for item in items]
            quantiles = (
                ("q05", 0.05), ("q25", 0.25), ("median", 0.5),
                ("q75", 0.75), ("q95", 0.95),
            )
            for name, quantile in quantiles:
                row[f"{feature}_{name}"] = round(percentile(values, quantile), 3)
            row[f"{feature}_mean"] = round(sum(values) / len(values), 3)
        for category in CATEGORIES:
            counts = metadata[(label, category)]
            top_values = counts.most_common(8)
            parts = [f"{value}={count}" for value, count in top_values]
            other_count = sum(counts.values()) - sum(count for _, count in top_values)
            if other_count:
                parts.append(f"other={other_count}")
            row[f"{category}_counts"] = "; ".join(parts)
        summary.append(row)
    write_csv(args.output / "class_summary.csv", summary, list(summary[0]))
    draw_profiles(args.output / "class_profiles.png", groups)

    print(
        f"Profiled {len(records)} images across {len(groups)} classes; "
        f"skipped {skipped} unreadable files."
    )
    print(f"Reports: {args.output}")


if __name__ == "__main__":
    main()
