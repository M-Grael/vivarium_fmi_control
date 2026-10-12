from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso

df = clean_sheet()

print(df.head())

estabilidade_de_peso(df)
evolucao_peso(df, show_plot=False)
