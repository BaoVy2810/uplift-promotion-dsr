# Uplift-Based Promotion Personalization for E-commerce

**From Prediction to Prescription: Designing an Uplift-Based Promotion Personalization System for E-commerce – A Design Science Approach**

## 1. Project Overview

This project investigates how uplift modeling can support personalized promotion decisions in e-commerce.

Traditional promotion targeting often relies on purchase propensity, identifying customers who are most likely to buy. However, customers with high purchase propensity may purchase even without receiving a promotion.

This research shifts the focus from predicting **who will buy** to estimating **who will buy because of the intervention**.

The project applies Design Science Research (DSR) to design, develop, and evaluate an uplift-based promotion decision support system.

The proposed system aims to support marketing decisions under budget and cost constraints while considering incremental conversions, incremental profit, and customer data protection.

## 2. Research Objectives

- Review and synthesize existing research on uplift modeling, causal inference, and promotion targeting.
- Compare random, propensity-based, uplift-based, and profit-based targeting policies.
- Evaluate uplift models using public randomized controlled trial (RCT) datasets.
- Design and develop an e-commerce promotion decision support artefact.
- Evaluate the artefact with marketing and e-commerce experts.

## 3. Research Questions

**RQ1:** Under the same budget constraints and different cost structures, which targeting policy (random, propensity, uplift, or profit-based uplift) generates the highest incremental conversions and incremental profit?

**RQ2:** How do different uplift estimation methods compare in effectiveness and stability across datasets with different characteristics? Which behavioral features explain treatment responsiveness?

**RQ3:** Is the proposed artefact useful, easy to use, and trustworthy for marketing and e-commerce decision-making according to expert evaluations?

## 4. Research Methodology

The research follows Design Science Research (DSR), using the Design Science Research Methodology (DSRM).

The evaluation consists of two main layers:

1. **Offline evaluation:** Experimental comparisons using public randomized datasets, with baselines, evaluation metrics, and confidence intervals.
2. **Artefact evaluation:** Expert evaluation of the promotion engine and decision-support dashboard.

## 5. Datasets

| Dataset | Role | Main characteristics |
|---|---|---|
| Hillstrom | Preliminary exploration and generalization | Email marketing experiment; approximately 64,000 customers |
| X5 RetailHero | Main dataset | Retail communication intervention; historical purchase records |
| Criteo Uplift | Scalability and stability evaluation | Large-scale online advertising experiment |

Public research datasets are stored locally and are not committed to this repository.

Dataset sources, licenses, preprocessing procedures, and limitations are documented in `docs/data-cards/`.

## 6. Technology Stack

### Research and Machine Learning

- Python 3.11
- Pandas, NumPy, SciPy
- Scikit-learn
- scikit-uplift
- CausalML
- EconML
- LightGBM
- SHAP
- DuckDB / Polars
- MLflow
- JupyterLab

### Application (Planned)

- Angular – Web application
- Node.js – Business API
- FastAPI – Model serving
- MongoDB – Application database
- Docker Compose – Service orchestration

The application stack will be developed in a later stage. The current research workflow focuses on Python-based offline experimentation.

## 7. Repository Structure

```text
uplift-promotion-dsr/
│
├── README.md
├── CONTRIBUTING.md             # Git workflow and code conventions
├── LICENSE
├── .gitignore
├── .env.example
├── environment.yml             # Python environment configuration
├── environment-lock.yml        # Resolved environment snapshot
├── docker-compose.yml          # Planned application orchestration
│
├── data/                       # Research datasets (not committed)
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── lab/                        # Offline research and experiments
│   ├── notebooks/
│   │   └── 01_hillstrom_eda.ipynb
│   ├── src/
│   │   └── uplift_lab/
│   ├── configs/
│   ├── tests/
│   └── reports/
│       ├── figures/
│       └── tables/
│
├── app/                        # Application components (planned)
│   ├── web/                    # Angular frontend
│   ├── api/                    # Node.js business API
│   └── model-service/          # FastAPI model service
│
├── docs/
│   ├── research-log/           # Weekly research progress
│   ├── decisions/              # Research and technical decisions
│   ├── data-cards/             # Dataset documentation
│   └── analysis_plan.md        # Experimental analysis plan
│
└── references/
    └── library.bib             # Bibliography exported from Zotero
```

## 8. Environment Setup

### 8.1 Prerequisites

- Git
- Conda (Miniconda or Anaconda)
- Python 3.11
- Node.js and npm (for the application, when implemented)
- Docker and Docker Compose (for later service integration)

### 8.2 Clone the Repository

```bash
git clone https://github.com/BaoVy2810/uplift-promotion-dsr.git

cd uplift-promotion-dsr
```

### 8.3 Create the Python Environment

Create the environment from the project configuration:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate uplift-promotion-dsr
```

### 8.4 Register the Jupyter Kernel

```bash
python -m ipykernel install --user \
    --name uplift-promotion-dsr \
    --display-name "Python 3.11 - Uplift Promotion DSR"
```

### 8.5 Launch JupyterLab

```bash
jupyter lab
```

Select the kernel:

`Python 3.11 - Uplift Promotion DSR`

### 8.6 Environment Reproducibility

- `environment.yml` provides the primary environment configuration for setting up the project.
- `environment-lock.yml` records the resolved packages and versions from the current environment.
- Update the environment configuration whenever important dependencies change.

The primary setup instruction is to use `environment.yml`. The lock file is provided as an additional reproducibility reference.

## 9. Running the Research Notebooks

Research notebooks are organized sequentially under `lab/notebooks/`.

| Notebook | Description | Status |
|---|---|---|
| `01_hillstrom_eda.ipynb` | Exploratory data analysis of Hillstrom | In progress |
| `02_eda_x5.ipynb` | Exploratory data analysis of X5 RetailHero | Planned |
| `03_eda_criteo.ipynb` | Exploratory data analysis of Criteo | Planned |
| Future notebooks | Feature engineering, model training, and evaluation | Planned |

Before running the notebooks:

1. Set up the Python environment.
2. Download the required dataset from its original source.
3. Review the corresponding dataset documentation in `docs/data-cards/`.
4. Place the dataset in the appropriate local directory under `data/raw/`.

Raw datasets should not be modified directly.

## 10. Reproducibility

To support reproducible research:

- Fix and document random seeds for experiments.
- Record package versions and environment configurations.
- Separate raw, intermediate, and processed datasets.
- Calculate behavioral features using only information available before treatment.
- Document research decisions in `docs/decisions/`.
- Record weekly progress in `docs/research-log/`.
- Predefine the analysis procedure before model training.
- Track model experiments using MLflow.

Reusable functions should be implemented in `lab/src/uplift_lab/` rather than duplicated across notebooks.

## 11. Data Privacy and Security

- Public datasets are not committed to GitHub.
- Personal access tokens, passwords, API keys, and `.env` files must not be committed.
- Research datasets are kept separate from the application's MongoDB database.
- The application is designed to minimize collected customer information and support consent management.
- No sensitive personal attributes are used for promotion targeting.

## 12. Git Workflow and Code Conventions

This project follows a structured Git workflow and consistent coding conventions.

For detailed instructions, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

Key principles:

- Keep `main` stable.
- Use descriptive branch names and commit messages.
- Follow Conventional Commits.
- Follow PEP 8 for Python code.
- Use descriptive variable and function names.
- Keep reusable logic in Python modules.
- Document research assumptions and experimental decisions.
- Never commit research datasets, secrets, or temporary files.

## 13. Current Research Status

**Current phase:** Research preparation and preliminary data exploration.

| Task | Status |
|---|---|
| Research brief | Completed – revision in progress |
| Literature review | 6/15 papers – expanding |
| Zotero organization | In progress |
| GitHub repository | Initial setup |
| Python environment | Initial setup completed |
| Hillstrom EDA | In progress |
| X5 data exploration | Pending |
| Criteo data exploration | Pending |
| Uplift model experiments | Not started |
| Web application | Not started |

## 14. Project Documentation

| Directory / File | Description |
|---|---|
| `docs/research-log/` | Weekly research progress |
| `docs/decisions/` | Research and technical decision records |
| `docs/data-cards/` | Dataset documentation and usage restrictions |
| `docs/analysis_plan.md` | Predefined experimental analysis plan |
| `references/library.bib` | Bibliography exported from Zotero |
| `CONTRIBUTING.md` | Git workflow and code conventions |

## 15. License

This project is released under the MIT License. See `LICENSE` for details.

---

**Author:** Trần Ngọc Bảo Vy - K234111461 - K234112E

**Institution:** University of Economics and Law (UEL)

**Research Area:** E-commerce, Uplift Modeling, Causal Inference, Design Science Research