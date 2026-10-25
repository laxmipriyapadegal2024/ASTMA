from __future__ import annotations

import pandas as pd
import streamlit as st

from src.data.validation import validate_dataset
from src.models.predict import analyze_post

st.title("Batch Analysis")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    issues = validate_dataset(df)

    st.subheader("Dataset validation")
    st.write(issues)

    if issues["errors"]:
        st.error("The dataset is invalid and cannot be analyzed until required columns are present.")
    else:
        rows = []
        for _, row in df.iterrows():
            text = str(row.get("text", "")).strip()
            if not text:
                continue
            analysis = analyze_post(text)
            rows.append({
                "post_id": row.get("post_id", ""),
                "text": text,
                "engagement_label": analysis["engagement"]["predicted_label"],
                "engagement_indicators": "; ".join(analysis["engagement"]["detected_indicators"]),
                "manipulation_labels": "; ".join(analysis["manipulation"]["labels"]),
                "claim_count": len(analysis["claims"]),
            })

        results_df = pd.DataFrame(rows)
        st.dataframe(results_df, width="stretch")

        csv_bytes = results_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download results CSV", data=csv_bytes, file_name="batch_analysis_results.csv", mime="text/csv")
