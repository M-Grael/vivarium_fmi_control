from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso, peso_alvo


df = clean_sheet()

print(df.head())
print(df.info())

estabilidade_de_peso(df, show_plot=True)
evolucao_peso(df, show_plot=True)
peso_alvo(df, show_plot=True)

