from os.path import join
from datetime import date
import pandas as pd

def clean_sheet():
    ID_DA_PLANILHA = '1m1PifIJZ2mVyv-Aqw6ntu8zyivUMqOhOP3lAV7WFuwQ'
    url_csv = f'https://docs.google.com/spreadsheets/d/{ID_DA_PLANILHA}/export?format=csv'

    df = pd.read_csv(url_csv)

    # 1. Seleção e renomeação
    df = df[[
        'Carimbo de data/hora',
        'Número do Rato',
        'Peso em gramas',
        'Observações',
    ]]
    df = df.rename(
        columns={
            'Carimbo de data/hora': 'carimbo',
            'Número do Rato': 'id',
            'Peso em gramas': 'peso',
            'Observações': 'obs',
        }
    )

    # 2. Tipagem
    df['carimbo'] = pd.to_datetime(df['carimbo'], dayfirst=True)
    df['data'] = pd.to_datetime(df['carimbo'].dt.date)

    for col in ['id', 'peso']:
        df[col] = df[col].astype(int)

    df['obs'] = df['obs'].fillna('---').astype(str)

    df = df.drop_duplicates(subset=['data', 'id'], keep='last')

    experiment_range = pd.date_range(
        start=df['data'].min(), end=pd.to_datetime(date.today())
    )

    dates_df = pd.MultiIndex.from_product(
        [experiment_range, range(1, 19)], names=['data', 'id']
    ).to_frame(index=False)

    df = pd.merge(dates_df, df, on=['data', 'id'], how='left')

    df['obs'] = df['obs'].fillna(
        'Não houve pesagem nessa data'
    )

    df = df[['carimbo', 'data', 'id', 'peso', 'obs']]
    df = df.sort_values(by=['data', 'id']).reset_index(
        drop=True
    )
    return df

if __name__ == '__main__':
    df_res = clean_sheet()
    print(f'Dados processados com sucesso! Total de linhas: {len(df_res)}')
    print(df_res.head(20))