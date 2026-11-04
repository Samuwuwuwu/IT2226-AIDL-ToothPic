# IT2226 AIDL - Group 7

Dental-health project for Singapore: guided photo capture, image screening, understandable explanations, indicative treatment costs/subsidies, and clinic finding.

**Current stage: initial scaffold.** The shared dataset package is prepared; model training, agent tools, clinical collaborator and product name are not confirmed or implemented.

## Windows quick start

Requires Python 3.11+ and Node.js 22+.

```bat
setup-dev.bat
start-dev.bat
```

Web: http://localhost:5173
API health: http://127.0.0.1:8000/api/v1/health. Ctrl+C stops both. Run `validate-local.bat` for local checks. No CI/GitHub Actions.

## Layout

```text
apps/web/            React, TypeScript, Vite
services/api/        FastAPI and API tests
ml/notebooks/        Colab entry points
ml/src/aidl_ml/      Shared ML code (Colab)
data/                Local images (ignored by Git)
docs/                Architecture, dataset register, contribution evidence
scripts/dev.py       Managed frontend/API launcher
setup-dev.bat        Install development dependencies
start-dev.bat        Run both hot-reload servers
validate-local.bat   Explicit local tests/build
audit-data.bat       Count image-folder classes
AGENTS.md            Coding and commit conventions
```

See [ML setup](ml/README.md), [architecture](docs/ARCHITECTURE.md), [dataset register](docs/DATASETS.md), and [team contributions](docs/CONTRIBUTING.md).

Upload `data/processed/school_oral_v1_training_v1.zip` once to the group Drive `dataset/` folder and use that copy in Colab. Keep raw images and checkpoints out of Git; teammates log substantive AI assistance in their own commits.

Current backend contains a real health endpoint; the frontend only displays the planned features and actual API connection. It does not pretend screening or tools exist yet. The assignment documents conflict on assessment weeks; confirm with the lecturer.
