import matplotlib
matplotlib.use('Agg')  # Evita erro de interface gráfica no servidor

from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso, peso_alvo, exportar_excel
from enviar_email import enviar_relatorio

df = clean_sheet()

print(df.tail())
print(df.info())

estabilidade_de_peso(df, show_plot=False)
evolucao_peso(df, show_plot=False)
peso_alvo(df, show_plot=False)
exportar_excel(df)

enviar_relatorio()