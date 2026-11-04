# Colab training data

Use the single group dataset archive: `data/processed/school_oral_v1_training_v1.zip`. Upload it once to the shared Google Drive `dataset/` folder. In Colab, mount the shared Drive, extract the archive there, and point training code at the extracted root.

The archive includes images under `train/`, `val/` and `test/`, with lowercase snake_case class folders. Use its `manifest.csv`, `splits.csv` and `class_to_idx.json`; do not create new splits. Save checkpoints and training outputs in the shared Drive, not Git.
