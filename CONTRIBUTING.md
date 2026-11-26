# Contributing Guidelines

This document defines the Git workflow and coding conventions for the `uplift-promotion-dsr` project.

## 1. Git Workflow

### 1.1 Branch Naming

Use the following naming conventions:

| Branch | Purpose |
|---|---|
| `main` | Stable and reproducible project version |
| `dev` | Integration branch for ongoing development |
| `feature/<name>` | New features or experiments |
| `fix/<name>` | Bug fixes |
| `docs/<name>` | Documentation updates |
| `refactor/<name>` | Code restructuring |

Examples:
- `feature/hillstrom-eda`
- `feature/uplift-model`
- `fix/data-preprocessing`
- `docs/update-analysis-plan`

### 1.2 Commit Messages

Follow the Conventional Commits format:

`<type>: <short description>`

Common types:

| Type | Usage |
|---|---|
| `feat` | Add a new feature |
| `fix` | Fix a bug |
| `docs` | Update documentation |
| `refactor` | Refactor existing code |
| `test` | Add or update tests |
| `exp` | Add or update research experiments |
| `chore` | Maintenance and configuration |
| `style` | Formatting changes without logic changes |

Examples:

- `chore: initialize project environment`
- `docs: add Hillstrom dataset documentation`
- `exp: perform initial Hillstrom EDA`
- `feat: implement uplift model evaluation`
- `test: add profit calculation tests`

Commit messages should be concise, descriptive, and written in English.

### 1.3 Basic Git Workflow

Before starting work:

```bash
git checkout dev
git pull origin dev
```

Create a working branch:

```bash
git checkout -b feature/hillstrom-eda
```

After completing a task:

```bash
git status
git add <specific-files>
git commit -m "exp: perform initial Hillstrom EDA"
git push -u origin feature/hillstrom-eda
```

Merge completed work into `dev` through a Pull Request when possible.

Only merge stable, reviewed work into `main`.

Do not use `git push --force` on shared branches.

### 1.4 Files That Must Not Be Committed

Never commit:
- Raw, intermediate, or processed research datasets.
- API keys, passwords, access tokens, or `.env` files.
- Virtual environments and local caches.
- Temporary Jupyter checkpoint files.
- Large generated model artifacts unless explicitly required.

Use `.env.example` to document required environment variables without including actual secrets.

---

## 2. Python Code Conventions

### 2.1 General Style

- Follow PEP 8.
- Use 4 spaces for indentation.
- Use meaningful and descriptive names.
- Prefer clear, readable code over unnecessarily complex implementations.
- Keep functions focused on a single responsibility.
- Avoid hard-coded paths and unexplained numerical constants.

### 2.2 Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Variables | `snake_case` | `treatment_group` |
| Functions | `snake_case` | `calculate_uplift()` |
| Classes | `PascalCase` | `UpliftModel` |
| Constants | `UPPER_SNAKE_CASE` | `RANDOM_SEED` |
| Modules | `snake_case` | `data_preprocessing.py` |

### 2.3 Documentation

- Add docstrings to reusable functions and classes.
- Use comments to explain non-obvious decisions.
- Document assumptions, inputs, outputs, and important limitations.
- Keep research methodology and experimental decisions documented in `docs/`.

Example:

```python
def calculate_incremental_profit(
    uplift,
    margin,
    treatment_probability,
    incentive_cost,
    contact_cost,
):
    """Calculate expected incremental profit per customer."""
    return (
        uplift * margin
        - treatment_probability * incentive_cost
        - contact_cost
    )
```

### 2.4 Reproducibility

- Set and document random seeds for experiments.
- Record model parameters and evaluation metrics.
- Keep dataset descriptions and preprocessing decisions documented.
- Separate raw data, intermediate data, and processed data.
- Avoid modifying raw datasets directly.
- Keep reusable logic in `lab/src/uplift_lab/` instead of duplicating code across notebooks.

### 2.5 Notebook Conventions

- Use numbered notebook filenames to indicate execution order.
- Use Markdown cells to explain objectives, methodology, and findings.
- Keep notebooks focused on one analysis or experiment.
- Restart and run all cells before considering a notebook complete.
- Remove unnecessary outputs and temporary cells before committing.
- Move reusable functions into `lab/src/uplift_lab/`.

Examples:

- `01_hillstrom_eda.ipynb`
- `02_data_preprocessing.ipynb`
- `03_baseline_uplift_model.ipynb`
- `04_cost_sensitive_evaluation.ipynb`

---

## 3. Research and Experiment Management

- Document important methodological decisions in `docs/decisions/`.
- Maintain research progress in `docs/research-log/`.
- Store dataset descriptions and usage restrictions in `docs/data-cards/`.
- Keep the analysis plan updated in `docs/analysis_plan.md`.
- Report experimental results with the dataset version, model configuration, and evaluation metrics.

All experiments should be reproducible and traceable to their configurations and data sources.

---

## 4. General Principles

1. Keep the `main` branch stable.
2. Make small, focused, and descriptive commits.
3. Never commit confidential information or research datasets.
4. Prioritize reproducibility and documentation.
5. Keep code modular, readable, and testable.
6. Record important research decisions and experimental changes.