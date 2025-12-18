from langchain_core.tools import tool
from pathlib import Path
import pandas as pd
import os

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "medicines.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Could not find dataset at: {DATA_PATH}")

_movies_df = pd.read_csv(DATA_PATH)

@tool
def search_medicine_by_title(title: str) -> str:
    """
    Search for a medicine in the Kaggle dataset by full or partial title.
    
    Args:
        title: The medicine title or a fragment of a title to search for.
    
    Returns:
        A formatted string containing matched medicine and key fields.
    """
    
    if not title or not isinstance(title, str):
        return "Error: title parameter must be a non-empty string."

    matches = _movies_df[_movies_df["med_name"].str.contains(title, case=False, na=False)]

    if matches.empty:
        return f"No medicine found matching title: {title}"

    matches = matches.head(5)

    result_lines = []
    for _, row in matches.iterrows():
        result_lines.append(
            f"- Title: {row['med_name']}, Disease name: {row.get('disease_name', 'N/A')}, "
            f"Final price: {row.get('final_price', 'N/A')}"
        )

    return "\n".join(result_lines)