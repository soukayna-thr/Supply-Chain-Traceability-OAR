# **Supply Chain Traceability Pipeline**

# Overview

This project implements a **full data pipeline** for synthetic supply
chain traceability using **Open Automated Registry (OAR) data**. The
pipeline covers data extraction, cleaning, normalization, relational
structuring, analytics, AI-based duplicate detection, and final export.



# Features

-   **Synthetic Data Generation:** Generates companies and facilities
    for multiple Mediterranean countries (Morocco, Spain, Portugal,
    Italy, France, Greece, Malta)

-   **Data Cleaning & Normalization:** Cleans company and facility
    names, removes duplicates, ensures relational integrity

-   **Relational Structuring:** Builds company-facility relationships
    for downstream analysis

-   **Analytics Dashboards:** Generates charts such as companies by
    country and facilities per company

-   **AI Duplicate Detection:** Uses Sentence Transformers to detect
    potential duplicate companies

-   **Export & Reporting:** Saves cleaned, relational, and AI datasets
    in CSV & JSON formats

# Directory Structure

``` {.bash language="bash"}
supply-chain-traceability-oar/
|
|-- data/
|   |-- raw/                      # Raw datasets (Phase 1)
|   |-- processed/                # Cleaned datasets
|   |-- relational/               # Relational datasets
|   |-- analytics/                # Charts and plots
|   |-- ai/                       # Duplicate detection results
|
|-- logs/                         # Pipeline execution logs
|
|-- main.py                       # Main pipeline script
|-- p1_scrape_oar.py              # Phase 1: Data extraction
|-- p2_clean_companies.py         # Phase 2: Company cleaning
|-- p3_clean_facilities.py        # Phase 3: Facility processing
|-- p4_relational_builder.py      # Phase 4: Relational structuring
|-- p5_analytics_dashboards.py    # Phase 5: Analytics
|-- p6_ai_module.py               # Phase 6: AI duplicate detection
|-- p7_export_final.py            # Phase 7: Final export
|-- requirements.txt              # Python dependencies
```

# Requirements

## Python Version

**Python 3.10 or higher**

## Required Packages

-   pandas

-   numpy

-   matplotlib

-   seaborn

-   sentence-transformers

-   scikit-learn

## Installation



## Clone the Repository

To clone the GitHub repository, run the following command:

``` {.bash language="bash"}
git clone https://github.com/soukayna-thr/Supply-Chain-Traceability-OAR.git
cd supply-chain-traceability
```


Install dependencies via pip:

``` {.bash language="bash"}
pip install -r requirements.txt
```

# Installation

## Create Virtual Environment

``` {.bash language="bash"}
# Create virtual environment
python -m venv .venv

# Activate on Linux / macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

# Usage

## Run Complete Pipeline

``` {.bash language="bash"}
python main.py
```

## Output Locations

-   **Logs:** `logs/pipeline.log`

-   **Processed data:** `data/processed/`

-   **Relational data:** `data/relational/`

-   **Analytics:** `data/analytics/`

-   **AI results:** `data/ai/`

-   **Final export:** `data/final/`

# Pipeline Phases

## Phase 1: Data Extraction

Generates synthetic OAR data with companies and facilities across
Mediterranean countries.

## Phase 2: Company Cleaning

Normalizes company names, removes duplicates, and standardizes formats.

## Phase 3: Facility Processing

Cleans facility data and links facilities to their parent companies.

## Phase 4: Relational Builder

Creates relational structure between companies, facilities, and links.

## Phase 5: Analytics Dashboards

Generates visualizations including:

-   Companies by country distribution

-   Facilities per company analysis


## Phase 6: AI Duplicate Detection

Uses Sentence Transformers (`all-MiniLM-L6-v2`) to:

-   Compute embeddings of company names

-   Calculate pairwise similarities

-   Detect potential duplicates

-   Output results in CSV & JSON formats

## Phase 7: Final Export

Consolidates all processed data including cleaned datasets, relational
links, and AI results.

# Logging

The pipeline features:

-   Centralized logging with console and file output

-   UTF-8 encoding for Unicode characters

-   Timestamped entries for tracking execution

-   Automatic log file creation in `logs/` directory

# AI Duplicate Detection

## Technical Details

**Model:** all-MiniLM-L6-v2 (Sentence Transformers)\
**Method:** Cosine similarity on company name embeddings\
**Output:** Potential duplicates with similarity scores

Results include duplicate pairs with confidence scores, exportable in
CSV and JSON formats, with full integration into the main pipeline.

# Analytics & Visualizations

Generated charts include:

1.  **Companies by Country:** Bar chart showing distribution

2.  **Facilities per Company:** Analysis of facility counts


# Project Flow

The pipeline executes in the following sequence:

1.  **Phase 1:** Extract synthetic data

2.  **Phase 2:** Clean companies

3.  **Phase 3:** Clean facilities

4.  **Phase 4:** Build relations

5.  **Phase 5:** Generate analytics

6.  **Phase 6:** Detect AI duplicates

7.  **Phase 7:** Final export

`main.py` orchestrates the entire pipeline. Each phase has its own
module with a `run()` function. Logs and outputs are automatically
created in structured folders with timestamped files for
reproducibility.

## Data Source Disclaimer

This project uses a **synthetic dataset** that mimics the structure of data from **Open Supply Hub (OS Hub)**.

At the time of development, direct access to the full Open Supply Hub dataset was **not publicly available to all users**. For this reason, a synthetic data generation phase (Phase 1) was implemented to simulate realistic company and facility data while preserving the expected schema and relationships.

### Using Real Open Supply Hub Data

If access to real data from https://opensupplyhub.org/ is available, the pipeline can be easily adapted by:

- Replacing **Phase 1 (synthetic data generation)** with a real data ingestion step
- Ensuring the real dataset follows the same column structure (company name, country, industry, description, facilities, etc.)
- Keeping all subsequent phases (cleaning, relational structuring, analytics, AI module, and export) unchanged

This design ensures that the pipeline remains **modular, reusable, and scalable**, whether using synthetic or real-world data.




