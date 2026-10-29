from pathlib import Path

import pytest

from aidl_ml.audit import count_images


def test_counts_recursively_and_ignores_text(tmp_path: Path) -> None:
    caries = tmp_path / "Caries"
    normal = tmp_path / "Normal"
    (caries / "inner").mkdir(parents=True)
    normal.mkdir()
    (caries / "a.JPG").write_bytes(b"example")
    (caries / "inner" / "b.png").write_bytes(b"example")
    (caries / "readme.txt").write_text("ignore")
    (normal / "n.webp").write_bytes(b"example")
    assert count_images(tmp_path) == {"Caries": 2, "Normal": 1}


def test_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        count_images(tmp_path / "missing")
