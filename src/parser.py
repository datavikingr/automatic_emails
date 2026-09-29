import pandas as pd
from pathlib import Path

def parse_file(file_path: Path) -> list[dict]:
    """Read CSV or XLSX and return a list of row dicts.
    Expects columns: email, first_name, last_name (case‑insensitive).
    Additional columns are preserved.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"Data file missing: {file_path}")

    ext = file_path.suffix.lower()
    if ext in ".csv":
        df = pd.read_csv(file_path, dtype=str)
    elif ext in ".xlsx":
        df = pd.read_excel(file_path, dtype=str)
    else:
        raise ValueError(f"Unsupported data file type: {ext}")

    # Normalize column names to lower case for consistency
    df.columns = [c.strip().lower() for c in df.columns]
    required_cols = {"email", "first_name", "last_name"}
    if not required_cols.issubset(set(df.columns)):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Fill NaNs with empty strings to avoid issues in template rendering
    df.fillna("", inplace=True)

    return df.to_dict(orient="records")
