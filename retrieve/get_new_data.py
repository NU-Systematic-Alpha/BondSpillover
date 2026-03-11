import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = BASE_DIR / "new_excel_data" / "newYieldData.xlsx"

BRAZIL = "./new_excel_data/Brazil3.csv"
HK = "./new_excel_data/HK{0}.csv"
INDIA = "./new_excel_data/India{0}.csv"
JAPAN = "./new_excel_data/Japan{0}.csv"
MEXICO = "./new_excel_data/Mexico{0}.csv"
KOREA = "./new_excel_data/SouthKorea{0}.csv"
SWITZ = "./new_excel_data/Switzerland{0}.csv"
US = "./new_excel_data/US{0}.csv"


def get_yield(term: int):
    if term not in [1, 2, 3, 5]:
        print('invalid term')
        return

    term_s = f'{term} year'
    cols = ['US', 'UK', 'FRA', 'GER', 'AUS', 'INDO', 'KOREA', 'BRAZIL', 'MEXICO']
    cols_to_add = ['HK', 'INDIA', 'JAPAN', 'SWITZ']

    df = pd.read_excel(EXCEL_PATH, sheet_name=term_s, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df = df[df.index.notna()]
    df.columns = cols

    extra_data = [HK, INDIA, JAPAN, SWITZ]
    result = []
    for data in extra_data:
        df_extra = pd.read_csv(data.format(term), index_col=0)
        df_extra = df_extra.iloc[:, [0]]
        df_extra.index = pd.to_datetime(df_extra.index, format="%m/%d/%Y", errors="coerce")
        df_extra = df_extra[df_extra.index.notna()]
        result.append(df_extra)

    extra_df = pd.concat(result, axis=1)
    extra_df.columns = cols_to_add
    df = pd.concat([df, extra_df], axis=1)

    # if term == 1:
    #     df_mex = pd.read_csv(MEXICO.format(term), index_col=0)
    #     df_kor = pd.read_csv(KOREA.format(term), index_col=0)
    # elif term == 2:
    
    # elif term == 3:
        
    return df

df = get_yield(1)
print(df.head(), '\n')
print(df.tail())
