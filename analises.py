import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from os import makedirs
from os.path import join

def __roundup(x):
    return int(math.ceil(x / 50)) * 50
def __rounddown(x):
    return int(math.floor(x / 50)) * 50 

def estabilidade_de_peso(df):
    df['data'] = pd.to_datetime(df['data'])
    df = df.dropna(subset='peso')

    df = df.sort_values(by=['id', 'data']).reset_index(drop=True)

    mask_medida_inicial = df.groupby('id').cumcount() < 3
    df['estabilidade'] = np.where(mask_medida_inicial, 'estavel', None)

    estabilidade = df.groupby('id').tail(4).reset_index(drop=True)

    return df

def evolucao_peso(df, show_plot = False):
    import matplotlib.pyplot as plt
    df = df.copy()

    df['data'] = pd.to_datetime(df['data'])
    df = df.dropna(subset='peso')

    df = df.sort_values(by=['id', 'data']).reset_index(drop=True)
    df = df.groupby('id').tail(7).reset_index(drop=True)
    df['session_i'] = df.groupby('id').cumcount() + 1

    data_min = df['data'].min()
    data_max = df['data'].max()

    peso_max = __roundup(df['peso'].max())
    peso_min = __rounddown(df['peso'].min())

    fig, axes = plt.subplots(3, 6, figsize=(10, 5))
    axes = axes.flatten()
    for i, ax in enumerate(axes):

        df_rato = df[df['id'] == i + 1].copy()
        ax.scatter(df_rato['session_i'], df_rato['peso'], color='black', marker='s')
        ax.plot(df_rato['session_i'], df_rato['peso'], color='black', linewidth=1)

        ax.set_xlim(0.5, 7.5)
        ax.set_ylim(peso_min, peso_max)

        ax.set_yticks(range(peso_min, peso_max + 1, 25))
        ax.set_xticks([])

        if i == 0:
            ticks = ax.get_yticks()
            labels = [ticks[0]] + [''] * (len(ticks) - 2) + [ticks[-1]]
            ax.set_yticklabels(labels)
        else:
            ax.set_yticklabels([])

        label_text = f'nº = {i + 1}' if i == 0 else f'{i + 1}'
        ax.text(1.0, 1.0, label_text, transform=ax.transAxes, va='top', ha='right')


        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

    fig.suptitle(f'Peso em gramas das últimas 7 pesagens\n\n{data_min.day}/{data_min.month}/{data_min.year} — {data_max.day}/{data_max.month}/{data_max.year}')
    
    PATH_RESULTS = 'results'

    fig.tight_layout()
    if show_plot:
        plt.show()
    else:
        makedirs(PATH_RESULTS, exist_ok=True)
        plt.savefig(join(PATH_RESULTS, 'ultimas_sete_pesagens.png'), dpi=400)
    plt.close()


if __name__ == '__main__':
    from limpeza import clean_sheet
    df = clean_sheet()
    print(estabilidade_de_peso(df))
    evolucao_peso(df)
    plt.show()