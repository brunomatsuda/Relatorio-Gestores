import pandas as pd

def get_folha(path=r'data/folha.xlsx'):
    return pd.read_excel(path)
