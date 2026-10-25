from __future__ import annotations

import re
from typing import Any

import pandas as pd


def normalize_whitespace(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.strip()
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    return text.strip()


def duplicate_mask(df: pd.DataFrame, column: str = "text") -> pd.Series:
    if column not in df.columns:
        return pd.Series(False, index=df.index)
    mask = df[column].fillna("").astype(str).duplicated(keep="first")
    return mask


def prepare_text_for_model(value: Any) -> str:
    return clean_text(value)
