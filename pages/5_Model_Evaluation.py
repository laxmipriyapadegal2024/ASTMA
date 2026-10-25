from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.config import MODELS_DIR

st.title("Model Evaluation")

metrics_file = MODELS_DIR / "engagement_model_metrics.json"
if not metrics_file.exists():
    st.info("No trained model has been saved yet. Run the training script to generate evaluation metrics.")
else:
    data = json.loads(metrics_file.read_text(encoding="utf-8"))
    st.subheader("Dataset summary")
    st.write({
        "dataset_size": data.get("dataset_size"),
        "random_seed": data.get("random_seed"),
        "class_distribution": data.get("class_distribution"),
    })

    model_rows = []
    for model_name, model_data in data.get("models", {}).items():
        for split_name in ["validation", "held_out_test"]:
            metrics = model_data.get(split_name, {})
            model_rows.append({
                "model": model_name,
                "split": split_name,
                "accuracy": metrics.get("accuracy"),
                "precision": metrics.get("precision"),
                "recall": metrics.get("recall"),
                "f1": metrics.get("f1"),
                "support": metrics.get("support"),
            })

    if model_rows:
        comparison_df = pd.DataFrame(model_rows)
        st.subheader("Model comparison")
        st.dataframe(comparison_df, width="stretch")

    for model_name, model_data in data.get("models", {}).items():
        st.subheader(model_name)
        for split_name in ["validation", "held_out_test"]:
            metrics = model_data.get(split_name, {})
            st.markdown(f"**{split_name.replace('_', ' ').title()}**")
            st.write(metrics)
            cm = metrics.get("confusion_matrix")
            if cm:
                st.write("Confusion matrix (rows=true, cols=predicted):", cm)

    st.caption("These metrics are only as trustworthy as the data and labels they were trained on. Do not interpret them as proof that the system generalizes to real-world political discourse without a suitable labeled dataset.")
