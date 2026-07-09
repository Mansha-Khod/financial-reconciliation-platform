# Financial Reconciliation & Data Quality Analytics Platform

A production-style financial reconciliation and data quality analytics application built with Python, Pandas, Plotly, and Streamlit.

The platform validates, cleans, standardizes, matches, and reconciles General Ledger (GL) and Trial Balance (TB) datasets while generating KPIs, exception reports, and interactive dashboards.

---

## Demo

**Live Demo**

https://financial-reconciliation-platform.streamlit.app/

**Demo Video**

![demo_video](assets/demo.gif)


---

## Screenshots

### Dashboard

![dashboard_1](assets/screenshots/dashboard_1.png)
![dashboard_2](assets/screenshots/dashboard_2.png)
![dashboard_3](assets/screenshots/dashboard_3.png)

---

### Validation Summary

![validation](assets/screenshots/validation.png)

---

### KPI Dashboard

![kpi](assets/screenshots/kpi.png)


---

### Exception Report

![exception](assets/screenshots/exception.png)

---

## Features

- CSV file validation
- Schema validation
- Column standardization
- Missing value detection
- Duplicate detection
- Account name cleaning
- Amount cleaning & numeric conversion
- Alias matching
- Fuzzy account matching using RapidFuzz
- General Ledger aggregation
- Financial reconciliation
- Tolerance-based matching
- KPI generation
- Exception reporting
- Interactive Plotly dashboard
- CSV report export
- Streamlit interface

---

## Project Architecture

```
financial-reconciliation-platform/

│
├── app.py
├── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── outputs/
│   ├── charts/
│   └── reports/
│
├── src/
│   ├── config.py
│   ├── validation.py
│   ├── preprocessing.py
│   ├── matching.py
│   ├── reconciliation.py
│   ├── kpi.py
│   ├── exception_engine.py
│   └── visualization.py
│
├── requirements.txt
└── README.md
```

---

## Workflow

```
Upload Files
      │
      ▼
Validation
      │
      ▼
Cleaning & Standardization
      │
      ▼
Alias Matching
      │
      ▼
Fuzzy Matching
      │
      ▼
Aggregation
      │
      ▼
Reconciliation
      │
      ▼
KPI Generation
      │
      ▼
Exception Reports
      │
      ▼
Visualization Dashboard
```

---

## Technologies Used

- Python
- Pandas
- RapidFuzz
- Plotly
- Streamlit
- NumPy

---

## Installation

Clone the repository

```bash
git clone https://github.com/Mansha-Khod/financial-reconciliation-platform.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```

Run the command-line version

```bash
python main.py
```

---

## Reports Generated

The application automatically generates:

- Reconciliation Report
- Exception Report
- KPI Summary
- Top Mismatches Report

---

## KPIs

- Total Accounts
- Match Rate
- Total GL Amount
- Total TB Amount
- Net Difference
- Largest Variance Account

---

## Visualizations

- Reconciliation Status Distribution
- GL vs TB Comparison
- Top Account Variances
- Distribution of Reconciliation Differences

---

## Future Improvements

- Configurable reconciliation rules
- PDF report generation
- Excel report export
- User-defined tolerance
- Database integration
- Multi-file reconciliation

---

## Author

**Mansha Khod**

B.Sc. Data Science  
Mount Carmel College, Bangalore

GitHub: https://github.com/Mansha-Khod
