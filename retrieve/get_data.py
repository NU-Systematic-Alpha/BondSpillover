import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "excel_data" / "YieldData.xlsx"

def get_yield(term: int):
    term_s = f'{term} year'
    cols = ['UK', 'CAN', 'DBR', 'FRN', 'SWISS', 'SEK', 'NOR', 'AUD', 'ITL', 'US', 'CNY']
    df = pd.read_excel(EXCEL_PATH, sheet_name=term_s, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df = df[df.index.notna()]

    df.columns = cols
    # This is necessary because some sheets are missing first few rows of data
    df = df.truncate(before = pd.to_datetime('2016-2-18'))
    return df

