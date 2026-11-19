from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso


df = clean_sheet()

print(df.head())
print(df.info())

estabilidade_de_peso(df, show_plot=True)
evolucao_peso(df, show_plot=True)

prima = df[['data', 'id', 'peso']]
prima = prima[prima['id'].between(5, 10)]
prima = prima.pivot_table(values='peso', index='data', columns='id')
print(prima.tail(5))

