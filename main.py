from limpeza import clean_sheet
from analises import estabilidade_de_peso, evolucao_peso

df = clean_sheet()

print(df.head())

estabilidade_de_peso(df)
evolucao_peso(df, show_plot=False)


from pathlib import Path

# Substitua pelo caminho da sua pasta (ex: 'C:/Users/Nome/Documentos' ou './minha_pasta')
caminho_da_pasta = Path('.')

# Checa se a pasta existe antes de tentar ler
if caminho_da_pasta.exists() and caminho_da_pasta.is_dir():
    print(f"Lendo arquivos em: {caminho_da_pasta}\n")
    
    # Itera sobre todos os itens na pasta
    for item in caminho_da_pasta.iterdir():
        if item.is_file():
            print(f"📄 Arquivo: {item.name}")
        elif item.is_dir():
            print(f"📁 Pasta: {item.name}")
else:
    print("A pasta especificada não existe.")