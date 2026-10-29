from __future__ import annotations

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
except ModuleNotFoundError:
    px = None

from src.data.loaders import load_sample_dataset
from src.features.ngrams import extract_top_ngrams, summarize_engagement_patterns

st.title("Research Dashboard")

df = load_sample_dataset()
if df.empty:
    st.info("Add sample data to data/sample/sample_posts.csv to view dashboard metrics.")
else:
    st.subheader("Dataset overview")
    counts = df["engagement_bait_label"].astype(str).value_counts().reset_index()
    counts.columns = ["label", "count"]
    st.bar_chart(counts.set_index("label")["count"])

    if "topic" in df.columns and px is not None:
        fig = px.histogram(df, x="topic", title="Topic distribution")
        st.plotly_chart(fig, width="stretch")
    elif "topic" in df.columns:
        topic_counts = df["topic"].astype(str).value_counts()
        st.bar_chart(topic_counts)

    st.subheader("Top phrase patterns")
    phrase_frame = pd.DataFrame(
        extract_top_ngrams(df["text"].fillna("").astype(str).tolist(), n=2, top_k=12),
        columns=["phrase", "count"],
    )
    if not phrase_frame.empty:
        st.dataframe(phrase_frame, width="stretch")

    st.subheader("Engagement-pattern summary by label")
    summary = summarize_engagement_patterns(df)
    for label, details in summary.items():
        st.markdown(f"### {label}")
        phrase_summary = pd.DataFrame(
            [{"pattern": key, "posts_with_pattern": value} for key, value in details["phrases"].items()]
        )
        if not phrase_summary.empty:
            st.bar_chart(phrase_summary.set_index("pattern")["posts_with_pattern"])
        if details["top_ngrams"]:
            st.write("Top phrases:", details["top_ngrams"][:5])

    st.caption("These patterns are associative indicators only and do not prove deception or author intent.")
