# Test for Consultancy with the D&A Education Team

This repository contains the tasks for the **UNICEF Data and Analytics technical evaluation** for education.


# Before start, please read the CONTRIBUTING.md file to set up the repository.


## Repository Structure:

src/
└── consultancy_assessment/
    ├── data/                           # Raw data files
    │   └── 01_rawdata/
    │       └── GLOBAL_DATAFLOW_2018-2022.xlsx
    ├── documentation/                 # Project documentation
    │   ├── consultancy_assessment_report.docx
    │   └── population_weighted_coverage.png
    ├── notebook/                      # Jupyter notebooks and supporting files
    │   ├── __init__.py
    ├── scripts/                       # Python scripts for running the project
    │   ├── __init__.py
    │   ├── assessment.py              # Core assessment logic
    │   ├── file_loader.py             # Data loading utilities
    │   └── run_project.py             # Entry point to run the project
    ├── user_profile.yaml              # Configuration or user-specific settings
    ├── utils.py                       # Utility functions
.gitignore                             # Files and directories to ignore in Git
.gitlab-ci.yml                         # GitLab CI/CD pipeline configuration
.pre-commit-config.yaml                # Pre-commit hook configuration
CONTRIBUTING.md                        # Instructions to configure the envirement
LICENSE
pyproject.toml
README.md



---

## Objective

This repository calculates the **population-weighted coverage** of two essential maternal health services:

- **Antenatal Care (ANC4)**  
  *% of women (aged 15–49) with at least 4 antenatal care visits*
  
- **Skilled Birth Attendance (SBA)**  
  *% of deliveries attended by skilled health personnel*

These indicators are analyzed **for countries classified as "on-track" or "off-track"** in achieving under-five mortality targets (as of 2022).

---

## ✅ Evaluation Focus

This technical assessment emphasizes your ability to:

-  **Structure reproducible and organized workflows**
-  **Collaborate effectively in shared environments**
-  **Apply rigorous data handling and analysis practices**

---

##  Workflow Overview

### 1. **Data Preparation**
- Clean and merge data using consistent country identifiers.
- Filter ANC4 and SBA coverage estimates for **years 2018–2022**.
- Keep **most recent coverage value per country** within this range.

### 2. **Weighted Analysis**
- Calculate **population-weighted coverage** for ANC4 and SBA.
- Use **2022 projected births** as weights.
- Perform the analysis separately for:
  - Countries **on-track**
  - Countries **off-track**

### 3. **Reporting**
- Generate a final Word report and coverage visualization.
- Output saved in the `documentation/` folder.

---


After the virtual env is setted up to run the end to end pipeline just run

```bash
    python src/consultancy_assessment/run_project.py 
```

and in the documentation folder will create the report with all the results.


Position I applied for: Household Survey Data Analyst Consultant - Req. #581656