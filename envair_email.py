import os
import smtplib
from datetime import date
from email.message import EmailMessage
from pathlib import Path

PATH_RESULTS = Path('results')

ARQUIVOS = [
    'diferca_estabilidade.png',
    'ultimas_sete_pesagens.png',
    'peso_alvo.png',
    'pesos.xlsx',
]

def enviar_relatorio():
    remetente = os.environ['EMAIL_REMETENTE']
    senha = os.environ['EMAIL_SENHA']
    # Lista de e-mails separados por vírgula no Secret do GitHub
    destinatarios = [
        email.strip()
        for email in os.environ['EMAIL_DESTINATARIOS'].split(',')
        if email.strip()
    ]

    hoje = date.today().strftime('%d/%m/%Y')

    msg = EmailMessage()
    msg['Subject'] = f'Relatório diário de pesagem - {hoje}'
    msg['From'] = remetente
    msg['To'] = ', '.join(destinatarios)
    msg.set_content(
        f'Olá,\n\nSeguem em anexo as análises atualizadas de pesagem do dia {hoje}.\n'
    )

    for nome_arquivo in ARQUIVOS:
        caminho = PATH_RESULTS / nome_arquivo
        if not caminho.exists():
            print(f'Aviso: arquivo não encontrado: {caminho}')
            continue

        if caminho.suffix == '.png':
            maintype, subtype = 'image', 'png'
        elif caminho.suffix == '.xlsx':
            maintype, subtype = (
                'application',
                'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        else:
            maintype, subtype = 'application', 'octet-stream'

        with open(caminho, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype=maintype,
                subtype=subtype,
                filename=nome_arquivo,
            )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)

    print(f'E-mail enviado com sucesso para {len(destinatarios)} destinatário(s)!')