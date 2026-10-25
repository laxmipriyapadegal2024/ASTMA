from __future__ import annotations

import pandas as pd
import streamlit as st

from src.models.predict import analyze_post

st.title("Single Post Analyzer")

post_text = st.text_area("Paste a post or headline", height=180, placeholder="Example: Share this now before they remove it! Officials say sanctions are being prepared.")
source_url = st.text_input("Source URL (optional)")
topic = st.text_input("Topic or event name (optional)")

if st.button("Analyze post"):
    if not post_text.strip():
        st.warning("Please enter a post for analysis.")
    else:
        result = analyze_post(post_text, source_url=source_url, topic=topic)

        st.subheader("Engagement-bait assessment")
        st.write(result["engagement"])

        st.subheader("Manipulation assessment")
        st.write(result["manipulation"])

        st.subheader("Claim extraction and evidence status")
        if not result["claims"]:
            st.info("The text does not contain a clear factual claim for verification.")
        else:
            for claim in result["claims"]:
                st.markdown(f"- **Claim:** {claim['text']}")
                st.write(claim)

        st.caption("Note: this result shows demo analysis and should be reviewed by a human analyst before any publication or decision.")
