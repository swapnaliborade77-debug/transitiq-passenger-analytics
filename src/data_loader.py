from pathlib import Path
import pandas as pd

def load_data(source) -> pd.DataFrame:
    if hasattr(source, "read"):
        source.seek(0)
        return pd.read_csv(source)
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)
