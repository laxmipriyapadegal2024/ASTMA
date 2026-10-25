# Detecting Politically Manipulative Engagement Bait and Misleading Narratives

## Overview

This project implements a transparent, modular Streamlit application for analyzing short social-media posts in the domain of global politics and foreign affairs. The system explicitly separates three assessment dimensions:

1. Engagement bait
2. Manipulation indicators
3. Factual claim evidence status

The application is designed for educational and research use, not for automated conclusions about political truth or intent.

## Project goals

- Detect explicit calls for likes, shares, comments, tags, and reposts.
- Flag common manipulative techniques without treating disagreement or emotion as proof of misinformation.
- Extract or identify claim-like statements and assess what evidence exists.
- Provide a practical demo pipeline with sample data and tests.

## MVP status

This repository implements the Phase 1 MVP, including:

- Streamlit frontend
- Single-post analysis
- CSV batch analysis
- Rule-based engagement and manipulation classifiers
- Claim extraction and evidence labeling
- Dataset validation and sample data
- Training/evaluation scripts
- Automated tests

## Folder structure

- `app.py` — main Streamlit entry point
- `pages/` — analysis pages
- `src/` — project logic
- `data/` — sample and prepared datasets
- `scripts/` — validation, training, and evaluation commands
- `tests/` — pytest tests
- `reports/` — methodology and report outlines

## Installation

### Windows

```powershell
cd c:\Users\Lakshmi\ASTMA
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS/Linux

```bash
cd /path/to/ASTMA
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Launch the app

```bash
streamlit run app.py
```

## Data preparation

Place a CSV at `data/sample/sample_posts.csv` or `data/raw/posts.csv` with columns such as:

- `post_id`
- `text`
- `topic`
- `engagement_bait_label`
- `manipulation_labels`

The sample file included in the repo is synthetic demo data and should be treated as such.

## Data ingestion and dataset sources

The project includes a structured ingestion workflow in [src/data/ingestion.py](src/data/ingestion.py). It normalizes schema variants, preserves separate label fields, removes exact duplicate posts, and documents public dataset candidates.

Recommended datasets to review before training on real data:

- LIAR
- FEVER
- MultiFC
- Public clickbait or engagement-bait corpora only when licensing and task fit are confirmed

These sources are complementary, not interchangeable:

- LIAR and FEVER are claim-verification resources.
- Clickbait corpora are not automatically political engagement-bait datasets.
- Political truth labels must not be collapsed into engagement-bait labels.

## Training and evaluation

```bash
python scripts/validate_dataset.py --input data/sample/sample_posts.csv
python scripts/train_models.py --input data/sample/sample_posts.csv
python scripts/evaluate_models.py --input data/sample/sample_posts.csv
```

The baseline comparison implemented in the project compares:

- Rule-based heuristic baseline
- TF-IDF + Logistic Regression
- TF-IDF + Linear SVM

## Tests

```bash
python -m pytest -q
```

## Important limitations

- This is a rule-based MVP and not a validated real-world classifier.
- It does not infer political truth from ideology or partisanship.
- No claim is presented as verified without evidence.
- Fact-checking integrations are optional and disabled unless API credentials are configured.

## Ethical use

This tool is intended to support careful research, journalism, and public-interest analysis. It should not be used to dehumanize political actors, target nationality or ideology, or generate unsupported accusations.
