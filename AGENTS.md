# IT2226 AIDL Group 7 — coding-agent guide

Four-person assessed prototype. Prefer a small, explainable, complete user flow over speculative infrastructure. Product naming, model choice and datasets remain provisional.

## Read first
- `README.md` — setup and actual implementation status.
- `docs/ARCHITECTURE.md` — responsibility boundaries.
- `docs/DATASETS.md` — what data is genuinely available.
- `ml/README.md` — Colab and local execution.
- `docs/CONTRIBUTING.md` — individual contributions.

## Source of truth
- `apps/web/`: React/Vite UI, camera interactions. Browser network requests stay in `src/services/api.ts`.
- `services/api/`: FastAPI, server-only provider integrations, deterministic fee rules, inference and agent tools when implemented. Routes remain thin.
- `ml/src/aidl_ml/`: reusable model training/evaluation code; Colab notebooks only drive this same code.
- `data/`: local-only and gitignored. Document source, label and split provenance separately.
- Never claim trained results, clinic integrations or model confidence that is not measured. Do not silently replace the mandatory six-class dataset with another dataset.
- Keep ML GPU dependencies out of the FastAPI environment. No model training on HTTP requests.

## Practical constraints
- No Docker/Kubernetes, CI, GitHub Actions, speculative microservices or MLOps platform. **Do not create `.github/workflows/`.**
- Use `setup-dev.bat`, `start-dev.bat` and `validate-local.bat` for local work.
- Never commit `.env`, keys, private dental images, downloaded checkpoints or large generated reports.
- Make a small coherent change, update affected documentation, state what was tested or not.

## Commits, attribution, and handoffs
- Everyone commits from their own GitHub identity and maintains an individual AI-use log (see `docs/AI_USE_LOG_TEMPLATE.md`).
- Use Conventional Commits: `<type>(<scope>): <concise summary>`.
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`. Typical scopes: `web`, `api`, `ml`, `data`, `agent`, `dev`.
- Example: `feat(ml): add dataset class distribution audit`.
- End coding-agent handoffs with a concise summary, tests run/skipped, and **exactly one suggested Conventional Commit message**. Do not auto-commit unless explicitly asked.
- The assessed author must be able to explain and modify their code, including AI-generated code.
