from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


df = clean_sheet()

print(df.head())
print(df.info())

estabilidade_de_peso(df, show_plot=False)
evolucao_peso(df, show_plot=False)

