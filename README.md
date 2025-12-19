# 📊 Twitter-Performance-Risk-Analysis

## Project Overview

This project is a performance analytics case study focused on using unstructured social media data to inform **competitive strategy** and proactively identify **market risks**. The primary objective is to demonstrate robust ETL procedures necessary for deriving reliable, high-value business insights from messy, real-time data sources.

---

## 🎯 Business Objective (High-Value Focus)

The core business question driving this analysis is:

> **"How can Twitter data analytics be used to measure competitors' brand communication effectiveness and identify real-time market risk anomalies?"**

---

## 🛠️ Key Skills Demonstrated

| Skill | Evidence in this Project |
| :--- | :--- |
| **Advanced DAX & Business Logic** | Creation of verifiable metrics (KPIs) and risk scores to track sentiment, engagement trends, and anomaly detection. |
| **Stakeholder Communication & Consulting** | Documentation that translates technical ETL decisions into business rationale and final strategic recommendations (this README). |
| **Robust ETL Data Modeling (Power Query)** | Extensive use of Power Query M-code for text cleaning, feature engineering, and data validation necessary for reliable sentiment and trend analysis. |
| **SQL Querying & Data Validation** | *(To be added: Outline of SQL principles used for data integrity checks.)* |
| **Version Control (Git)** | Maintenance of a reliable audit trail for all code changes and documentation using GitHub. |

---

## Methodology & ETL Pipeline

graph TD
    subgraph Sourcing
    A[(Kaggle: ChatGPT Twitter Data)] --> B[Data Cleaning]
    end

    subgraph ETL_Process
    B --> C[Handle Missing Values: 'Unknown']
    C --> D[Column Filtering & Optimization]
    D --> E{Feature Engineering}
    E --> F[Tweet_Date: Daily Trends]
    E --> G[Tweet_Hour: Anomaly Detection]
    end

    subgraph Analysis
    F --> H[Risk Analysis Model]
    G --> H
    end

### 1. Data Sourcing & Cleaning (In Progress)

* **Source:** Daily ChatGPT Twitter data (Kaggle).
* **Initial Integrity & Cleanup:** To ensure reliable analysis, negligible data errors were removed, and high-volume missing categorical values were replaced with **"Unknown."** This prevents data loss while allowing users to analyze the impact of incomplete source data.
* **Noise Reduction & Focus:** Irrelevant columns were removed (early filtering) to **optimize Power Query performance** and focus the model solely on risk-analysis fields.
* **Date/Time Integrity & Optimization:** The primary timestamp (`tweet_created`) was used to derive two key dimensions: `Tweet_Date` (for daily trends) and a dedicated **`Tweet_Hour`** (for real-time anomaly detection). This optimization ensures the data is correctly structured for the core business objective of spotting hourly risk spikes.

### 2. Analysis & Risk Identification


### 3. Final Recommendation

