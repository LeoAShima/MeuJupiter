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

historico_handler = CommandHandler('historico', historico)
dispatcher.add_handler(historico_handler)

updater.start_polling()

def getHistorico():
    print("Obtendo histórico escolar")
    os.system("wget --save-cookies cookies.txt --keep-session-cookies --post-data 'codpes="+os.environ.get('CODPES')+"&senusu="+os.environ.get('SENUSU')+"&Submit+Entrar+&url=' --delete-after https://uspdigital.usp.br/jupiterweb/autenticar")
    os.system("wget --load-cookies cookies.txt -O HistoricoEscolar.pdf 'https://uspdigital.usp.br/jupiterweb/historicoescolarListar?cmd=cmd&codpgmclg=1%2FR%2F3&codcurhab=3032%2F3170%2FAtivo'")
