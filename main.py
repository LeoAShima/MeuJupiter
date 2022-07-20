import os
import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
updater = Updater(token=os.environ.get('BOT_TOKEN'))
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="historico")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def historico(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Obtendo histórico escolar...")
    getHistorico()
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('HistoricoEscolar.pdf', 'rb'))

def acompCred(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Obtendo total de créditos...")
    getAcompCred()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('acompCred.png', 'rb'))

historico_handler = CommandHandler('historico', historico)
acompCred_handler = CommandHandler('acompCred', acompCred)
dispatcher.add_handler(historico_handler)
dispatcher.add_handler(acompCred_handler)

updater.start_polling()

def getHistorico():
    print("Obtendo histórico escolar")
    os.system("wget --save-cookies cookies.txt --keep-session-cookies --post-data 'codpes="+os.environ.get('CODPES')+"&senusu="+os.environ.get('SENUSU')+"&Submit+Entrar+&url=' --delete-after https://uspdigital.usp.br/jupiterweb/autenticar")
    os.system("wget --load-cookies cookies.txt -O HistoricoEscolar.pdf 'https://uspdigital.usp.br/jupiterweb/historicoescolarListar?cmd=cmd&codpgmclg=1%2FR%2F3&codcurhab=3032%2F3170%2FAtivo&opcclsturma=S'")

def getAcompCred():
    print("Obtendo total de créditos")
    os.system("wget --save-cookies cookies.txt --keep-session-cookies --post-data 'codpes="+os.environ.get('CODPES')+"&senusu="+os.environ.get('SENUSU')+"&Submit+Entrar+&url=' --delete-after https://uspdigital.usp.br/jupiterweb/autenticar")
    os.system("wget --load-cookies cookies.txt -O acompCred.png 'https://uspdigital.usp.br/jupiterweb/GraphicControle?tipografico=barGrupoDesempenho&codpgm=1&sequencia=0'")
