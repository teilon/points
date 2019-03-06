import pandas as pd
import re


def read_file(filename):
    df = get_df_by_file(filename)

    # df['number'] = df['article'].apply(get_aromaname)
    # df['type'] = df['number'].apply(lambda x: x[0])
    # groupped = df.groupby(['region', 'station'])['real'].sum()
    result = df[['name', 'address', 'payment', 'form']]
    return result


def get_df_by_file(filename):
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        print('FileNotFoundError')
