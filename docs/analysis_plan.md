# Analysis Plan

## 1. Research Objective

The objective of this study is to investigate cost-sensitive uplift modeling for e-commerce promotion decision-making.

The study aims to evaluate whether incorporating promotion-related costs into uplift-based targeting can improve campaign profitability compared with conventional uplift-based targeting strategies.

## 2. Research Questions

- How effectively can uplift models estimate the incremental impact of promotional interventions on customer purchasing behavior?
- How does incorporating contact and incentive costs affect customer targeting decisions?
- How does cost-sensitive uplift targeting compare with conventional uplift-based targeting in terms of incremental profit?

## 3. Dataset

The study will initially use the Hillstrom Email Marketing Dataset.

The dataset contains customer-level information and experimental marketing campaign outcomes. It includes treatment groups and customer purchase behavior, making it suitable for investigating uplift modeling.

Further data inspection will be conducted to identify:
- Available treatment groups.
- Customer-level features.
- Purchase-related outcome variables.
- Data quality issues and missing values.

## 4. Experimental Design

The analysis will follow the experimental treatment structure available in the dataset.

The treatment and control groups will be identified based on the dataset documentation and verified during exploratory data analysis.

The primary outcome will be customer purchase behavior.

The analysis will distinguish between:
- Treatment assignment.
- Observed customer outcomes.
- Estimated incremental treatment effects.

## 5. Modeling Approach

The study will investigate uplift modeling approaches and compare their performance.

Candidate approaches may include:
- Two-Model approach (T-Learner).
- Class Transformation approach.
- Other suitable uplift modeling methods, depending on implementation feasibility.

The final model selection will be documented with justification.

## 6. Cost-Sensitive Targeting

The targeting framework will consider the economic impact of promotional interventions.


The estimated incremental profit will be used to support customer targeting decisions:

$$
\Delta \Pi(i) = \tau(i)m - \delta p_T(i) - c
$$

Where:

- $\Delta \Pi(i)$: Estimated incremental profit from targeting customer $i$.
- $\tau(i)$: Estimated incremental treatment effect (uplift).
- $m$: Contribution margin per purchase before incentive costs.
- $\delta$: Incentive cost per treated purchase.
- $p_T(i)$: Estimated purchase probability under treatment.
- $c$: Contact cost per targeted customer.

Cost assumptions and parameter values will be documented separately and subjected to sensitivity analysis where appropriate.

## 7. Evaluation Metrics

Model evaluation will consider both uplift performance and business value.

Potential evaluation metrics include:
- Qini coefficient.
- AUUC (Area Under the Uplift Curve).
- Uplift at different targeting proportions.
- Incremental profit.
- Cumulative profit and campaign cost.

The final metrics will depend on data suitability and the selected experimental design.

## 8. Experimental Procedure

The analysis will follow these stages:

1. Dataset inspection and exploratory data analysis.
2. Data preprocessing and feature preparation.
3. Treatment and outcome definition.
4. Model training and validation.
5. Uplift estimation and model evaluation.
6. Cost-sensitive targeting implementation.
7. Profit-based comparison and sensitivity analysis.
8. Interpretation of findings.

## 9. Reproducibility

All experiments will be conducted using documented configurations and reproducible code.

Research datasets will remain outside version control. Notebooks, source code, experiment configurations, and research documentation will be maintained in the repository.

## 10. Current Status

The project is currently in the initial environment setup and exploratory data analysis stage.

The analysis plan may be refined as dataset inspection, literature review, and experimental implementation progress.