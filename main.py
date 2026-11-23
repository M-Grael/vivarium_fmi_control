from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso, peso_alvo, exportar_excel


df = clean_sheet()

print(df.tail())
print(df.info())

estabilidade_de_peso(df, show_plot=True)
evolucao_peso(df, show_plot=True)
peso_alvo(df, show_plot=True)
exportar_excel(df)