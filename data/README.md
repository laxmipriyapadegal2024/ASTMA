# Dataset directory

This project includes a synthetic sample dataset that is intentionally labeled as demo data for the MVP. It is not a real-world social media corpus and should not be used to claim general model performance.

## Files

- `data/sample/sample_posts.csv` — demonstration dataset used by the application and tests.
- `data/raw/` — place manually downloaded or licensed datasets here.
- `data/processed/` — cleaned and prepared training datasets.

## Recommended normalized schema

The pipeline supports datasets with fields such as:

- `post_id`
- `text`
- `timestamp`
- `platform`
- `topic`
- `engagement_bait_label`
- `manipulation_labels`
- `claim_text`
- `claim_verdict`
- `evidence_source`
- `source_url`

## Supported public-source candidates

The project documents the following public sources as examples of relevant research datasets and evidence corpora:

- LIAR — political claim labeling and fact-check-oriented claim analysis
  - Link: https://www.cs.uic.edu/~liub/FakeNews/index.html
  - Intended task: political claim and verdict analysis
  - Caution: not a direct engagement-bait dataset

- FEVER — evidence-based claim verification
  - Link: https://fever.ai/dataset/fever.html
  - Intended task: claim verification with evidence and supporting documents
  - Caution: not a social-media engagement-bait corpus

- MultiFC — multi-domain fact-checking dataset
  - Link: https://github.com/ENCASEH2021/MultiFC
  - Intended task: claim verification and source evaluation
  - Caution: distinct from engagement-bait labeling

- Clickbait or engagement-bait corpora — only if they are licensable and explicitly fit the engagement solicitation task
  - Caution: clickbait labels are not the same as political engagement-bait labels

## Acquisition workflow

1. Download a dataset only from a publicly documented and licensed source.
2. Save it under `data/raw/` with a descriptive filename.
3. Validate the columns and label values before training.
4. Keep the human-annotated labels separate from model outputs and heuristic flags.
5. Store dataset provenance in a README or metadata file alongside the dataset.

## Manual ingestion command

```bash
python -c "from src.data.ingestion import ingest_dataset; print(ingest_dataset('data/sample/sample_posts.csv', source_name='synthetic_demo')['rows_loaded'])"
```

## Annotation workflow for missing engagement-bait labels

If a suitable public dataset is unavailable, use a transparent annotation guide with two annotators per post. Label the following separately:

- engagement solicitation
- manipulation techniques
- factual claim status
- insufficient context

Keep annotation disagreements and edge cases in the dataset notes instead of forcing a label.

## Licensing and usage limitations

- Review the license of every external dataset before training or publishing results.
- Never assume a dataset is acceptable for reused research without checking its terms.
- Do not treat political disagreement, emotional rhetoric, or criticism as proof of misinformation.
