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

def estabilidade_de_peso(df, show_plot = False):
    df = df.copy()

    df['data'] = pd.to_datetime(df['data'])
    df = df.dropna(subset='peso')
    df = (
        df.dropna(subset=['peso'])
        .sort_values(['id', 'data'])
        .reset_index(drop=True)
    )
    df = df.groupby('id').tail(4).reset_index(drop=True)
    df['session_i'] = df.groupby('id').cumcount() + 1

    media_3 = df[df['session_i'] <= 3].groupby('id')['peso'].mean()

    # map alinha pelo id, então cada linha recebe a média do seu id
    df['peso_estavel'] = df['id'].map(media_3)
    df['diff_estavel'] = df['peso'] / df['peso_estavel']

    fig, grafs = plt.subplots(6, 3, figsize=(8, 8))
    axes = grafs.flatten()
    for i, ax in enumerate(axes):

        df_rato = df[df['id'] == i + 1].copy()

        ax.fill_between([3.5, 4.5], 0.8, 1.2, color="#F78F8F", alpha=1)
        ax.fill_between([3.5, 4.5], 0.9, 1.1, color="#F8F7C4", alpha=1)

        if df_rato['diff_estavel'].iloc[-1] > 1.10:
            ax.set_facecolor("#FDFBC9")
        if df_rato['diff_estavel'].iloc[-1] < 0.9:
            ax.set_facecolor("#FDFBC9")
        
        ax.scatter(df_rato['session_i'], df_rato['diff_estavel'], color='black', marker='s')
        ax.plot(df_rato['session_i'][:3], df_rato['diff_estavel'][:3], color='black', linewidth=1)
        
        ax.set_ylim(0.8, 1.2)
        ax.set_xlim(0.5, 4.5)

        ax.set_xticks(range(1, 5))
        ax.set_xticklabels([])

        if i == 17:
            dias = pd.to_datetime(df_rato['data']).dt.strftime('%d/%m')
            ax.set_xticklabels(dias)

        if i == 0:
            ax.set_yticks([0.8, 1, 1.2])
        else:
            ax.set_yticks([])

        label_text = f'nº rato = {i + 1}' if i == 0 else f'{i + 1}'
        ax.text(0.01, 0.99, label_text, transform=ax.transAxes, va='top', ha='left')
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

    fig.suptitle('Diferença relativa da última pesagem em relação à estabilidade\nobservada nas três sessões anteriores')
    fig.supxlabel('Data da pesagem')


    fig.tight_layout()
    PATH_RESULTS = 'results'

    fig.tight_layout()
    if show_plot:
        plt.show()
    else:
        makedirs(PATH_RESULTS, exist_ok=True)
        plt.savefig(join(PATH_RESULTS, 'diferca_estabilidade.png'), dpi=400)
    plt.close()

def evolucao_peso(df, show_plot = False):
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
    plt.show()