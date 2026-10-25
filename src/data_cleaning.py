import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy().drop_duplicates()
    for col in ("route", "stop"):
        if col in result.columns:
            result[col] = result[col].astype("string").str.strip()
    if "passengers" in result.columns:
        result["passengers"] = pd.to_numeric(result["passengers"], errors="coerce").fillna(0).clip(lower=0)
    if "hour" in result.columns:
        result["hour"] = pd.to_numeric(result["hour"], errors="coerce").fillna(0).clip(0, 23).astype(int)
    return result.reset_index(drop=True)
