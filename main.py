from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso


df = clean_sheet()

print(df.head())
print(df.info())

estabilidade_de_peso(df, show_plot=False)
evolucao_peso(df, show_plot=False)

