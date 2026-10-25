from __future__ import annotations

import streamlit as st

from src.data.loaders import load_sample_dataset

st.set_page_config(page_title="Political Narrative Intelligence", layout="wide")
st.title("Political Narrative Intelligence")
st.caption("Detecting politically manipulative engagement bait and misleading narratives in social media.")

st.markdown(
    """
    This project separates three independent assessments:
    - Engagement bait: explicit requests for likes, comments, shares, or tags.
    - Manipulation: rhetorical pressure, urgency, fear, identity pressure, or conspiracy framing.
    - Factual status: whether the claim has support, contradiction, or is unverified.
    """
)

sample_df = load_sample_dataset()
if sample_df.empty:
    st.warning("No sample dataset is available yet. Add a CSV to data/sample/sample_posts.csv.")
else:
    st.subheader("Dataset status")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sample rows", len(sample_df))
    col2.metric("Engagement bait examples", int(sample_df["engagement_bait_label"].astype(str).str.contains("1|engagement_bait").sum()) if "engagement_bait_label" in sample_df.columns else 0)
    col3.metric("Model status", "Demo / untrained")

st.subheader("How to use")
st.markdown(
    """
    1. Open the post analyzer page and paste a social media post.  
    2. Upload a CSV in the batch analysis page.  
    3. Inspect claim verification, evaluation, and dashboard pages.  
    """
)

st.info(
    "This application is intentionally transparent: if a model is not trained, it clearly labels the result as demonstration mode instead of presenting inferred values as verified predictions."
)
