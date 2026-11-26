# Documentation Conventions

This folder contains research documentation, project decisions, analysis plans, and progress records for the thesis project.

The purpose of these conventions is to keep research activities transparent, organized, and reproducible throughout the project.

## 1. Folder Structure

```text
docs/
├── README.md
├── analysis_plan.md
├── research-log/
└── decisions/
```

| Path | Purpose |
|---|---|
| `README.md` | Explains documentation structure, naming conventions, and templates. |
| `analysis_plan.md` | Describes research objectives, questions, experimental design, modeling approach, and evaluation plan. |
| `data-cards/` | Detailed documentation, source terms, variable definitions and preliminary EDA findings summaries. |
| `decisions/` | Formal Decision Logs following DSRM guidelines. |
| `research-log/` | Records weekly research progress, activities, findings, and challenges. |
| `decisions/` | Documents important project and research decisions, including their rationale and alternatives. |

## 2. Research Log Naming Convention

Research logs use the following format:

```text
YYYY-Www.md
```

Where:
- `YYYY`: Four-digit year.
- `W`: Indicates the ISO week number.
- `ww`: Two-digit week number.

Each weekly log should document:
- Weekly objectives.
- Research activities completed.
- Evidence of completed work, such as commits, notebooks, MLflow runs, or files.
- Key results and findings.
- Problems, challenges, or unresolved questions.
- Decisions made during the week.
- Time spent on different activities.
- Questions for the supervisor.
- Planned activities for the following week.

A new file should be created for each research week. Use the template in Appendix A.

## 3. Decision Log Naming Convention

Decision records use the following format:

```text
D-XXX-short-description.md
```

Where:
- `D`: Stands for Decision.
- `XXX`: A three-digit sequential identifier.
- `short-description`: A short, descriptive title using lowercase words separated by hyphens.

Each decision record should include:

1. **Context:** The problem or situation requiring a decision.
2. **Alternatives:** Other options considered and their advantages or disadvantages.
3. **Decision:** The selected approach or solution.
4. **Rationale and Evidence:** Reasons and supporting evidence for the decision.
5. **Consequences:** Expected implications, trade-offs, risks, and monitoring plans.
6. **Status:** Proposed, Accepted, Superseded, or Rejected.

Decision IDs should remain unchanged once assigned. If an accepted decision is later revised, create a new decision record and reference the previous one rather than silently overwriting the original.

Use the template in Appendix B.

## 4. General File Naming Rules

To maintain consistency across the documentation:

- Use lowercase letters for filenames, except for decision identifiers such as `D-003`.
- Separate words using hyphens (`-`) in filenames.
- Use descriptive names that clearly indicate the document's purpose.
- Use `.md` for Markdown documentation.
- Use ISO week numbering (`YYYY-Www`) for weekly research logs.
- Keep existing file names and references consistent when updating documentation.

## 5. Documentation Maintenance

- Update the research log regularly, preferably at the end of each research week.
- Update `analysis_plan.md` whenever the research design or methodology changes materially.
- Record important methodological, technical, and project-management decisions in the `decisions/` folder.
- Keep documentation consistent with the actual implementation and research progress.
- Avoid recording sensitive information, credentials, or private data in this folder.

These conventions may evolve as the research project progresses. Any changes should be applied consistently across the repository.

---

# Appendix A. Weekly Research Log Template

**Filename:** `YYYY-Www.md`

Copy the following template when creating a new weekly research log.

```markdown
# Research Log: YYYY-Www (DD/MM – DD/MM/YYYY)

## Weekly Objectives
- ...

## Activities Completed

| Date | Activity | Evidence (commit / notebook / MLflow run / file) |
|------|----------|--------------------------------------------------|
|      |          |                                                  |

## Key Results
- ...

## Problems and Challenges
- ...

## Decisions Made This Week
- D-XXX: Brief description of the decision ([decision record](../decisions/D-XXX-short-description.md))

## Time Tracking (hours)

- Reading: _
- Data and Modeling: _
- Web Development: _
- Writing: _
- **Total: _**

## Questions for the Supervisor
- ...

## Plans for Next Week
- [ ] ...
```

---

# Appendix B. Decision Log Template

**Filename:** `D-XXX-short-description.md`

Copy the following template when documenting an important project or research decision.

```markdown
# D-XXX: Decision Title

**Date:** DD/MM/YYYY  
**Status:** Proposed / Accepted / Superseded / Rejected  
**Related:** Issue #X; Research Log YYYY-Www; relevant section or document

## Context

Describe why this decision is necessary.

Include relevant constraints, such as:
- Project requirements.
- Research objectives.
- Time constraints.
- Technical limitations.
- Available skills and resources.

## Alternatives Considered

1. **Option A**
   - Advantages:
   - Disadvantages:

2. **Option B**
   - Advantages:
   - Disadvantages:

## Decision

Describe the selected option and specify what will be implemented or followed.

## Rationale and Evidence

Explain why this option was selected.

Include supporting evidence where applicable, such as:
- Technical documentation.
- Research literature.
- Experiments or preliminary results.
- Project requirements.
- Supervisor feedback.

## Consequences

Describe the expected implications of this decision.

- Benefits:
- Trade-offs and limitations:
- Potential risks:
- Mitigation or monitoring plan:
```