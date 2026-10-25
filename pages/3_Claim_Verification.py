from __future__ import annotations

import json

import streamlit as st

from src.verification.claim_extraction import evaluate_claim_evidence

st.title("Claim Verification")

claim = st.text_area("Claim text")
manual_evidence = st.text_area("Evidence JSON or records", value='[\n  {"title": "Example evidence", "url": "https://example.com", "snippet": "Officials announced a new trade restriction yesterday.", "support": "support"}\n]')

if st.button("Assess claim"):
    try:
        evidence = json.loads(manual_evidence)
    except json.JSONDecodeError:
        evidence = []
        st.warning("Evidence did not parse as valid JSON; no automated evidence was assessed.")

    result = evaluate_claim_evidence(claim, evidence)
    st.subheader("Assessment")
    st.write(result)
