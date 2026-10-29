# ML workflow — Colab first, local alternative

`ml/src/aidl_ml/` is shared reusable Python source. Colab notebooks should import those functions rather than making the notebook the only training implementation.

**Current state:** a dataset folder-counting utility exists. A dataset loader, model, training pipeline, metrics and checkpoint have **not** been implemented.

## Colab
1. Choose a suitable Colab runtime when training begins.
2. Open `ml/notebooks/00_colab_setup.ipynb`.
3. Securely clone or upload your **private** repository into Colab. Never hardcode access tokens.
4. Set `REPO_ROOT`, then install `ml/` in editable mode.
5. Store large images on Drive / Colab storage rather than Git, and keep source/split details in `docs/DATASETS.md`.

## Optional local training

```bat
py -3 -m venv .venv-ml
.venv-ml\Scripts\python.exe -m pip install -e ml
.venv-ml\Scripts\python.exe -m aidl_ml.audit data\raw\oral-images
```

When actual training code is implemented, install PyTorch/torchvision in this **separate ML environment** using the correct CUDA instructions for the machine, not in `services/api/.venv`.

For a folder-per-class image dataset, `audit-data.bat data\raw\oral-images` prints class counts. It does not validate images, labels, permissions, duplicates or patient-level leakage.
