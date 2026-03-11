import pandas as pd
EXCEL_PATH = "./new_excel_data/newYieldData.xlsx"

BRAZIL = "./new_excel_data/Brazil{0}.csv"
HK = "./new_excel_data/HK{0}.csv"
INDIA = "./new_excel_data/India{0}.csv"
JAPAN = "./new_excel_data/Japan{0}.csv"
MEXICO = "./new_excel_data/Mexico{0}.csv"
KOREA = "./new_excel_data/SouthKorea{0}.csv"
SWITZ = "./new_excel_data/Switzerland{0}.csv"
US = "./new_excel_data/US{0}.csv"


def get_yield(term: int):
    if term not in [1, 2, 3, 5]:
        raise ValueError('invalid term')

    term_s = f'{term} year'
    cols = ['US', 'UK', 'FRA', 'GER', 'AUS', 'INDO', 'KOREA', 'BRAZIL', 'MEXICO']

    data_map = {
        'US': US,
        'KOREA': KOREA,
        'BRAZIL': BRAZIL,
        'MEXICO': MEXICO,
        'HK': HK,
        'INDIA': INDIA,
        'JAPAN': JAPAN,
        'SWITZ': SWITZ,
    }

    replace_map = {
        1: ['KOREA', 'MEXICO'],
        2: ['US'],
        3: ['BRAZIL'],
        5: ['BRAZIL', 'MEXICO']
    }

    cols_to_replace = replace_map.get(term)
    cols_to_add = ['HK', 'INDIA', 'JAPAN', 'SWITZ']
    cols_to_add.extend(cols_to_replace)

    df = pd.read_excel(EXCEL_PATH, sheet_name=term_s, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df = df[df.index.notna()]
    df.columns = cols

    df = df.drop(columns=cols_to_replace)

    result = []
    for col in cols_to_add:
        data = data_map.get(col)
        df_extra = pd.read_csv(data.format(term), index_col=0)
        df_extra = df_extra.iloc[:, [0]]
        df_extra.index = pd.to_datetime(df_extra.index, format="%m/%d/%Y", errors="coerce")
        df_extra = df_extra[df_extra.index.notna()]
        result.append(df_extra)

    extra_df = pd.concat(result, axis=1)
    extra_df.columns = cols_to_add
    df = pd.concat([df, extra_df], axis=1)
        
    return df
