import os
import logging
import re
import yaml
from telegram.ext import Updater, CommandHandler
import telegram

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

def periodoIdeal(update, context):
    os.system("wget --save-cookies cookies.txt --keep-session-cookies --post-data 'codpes="+os.environ.get('CODPES')+"&senusu="+os.environ.get('SENUSU')+"&Submit+Entrar+&url=' --delete-after https://uspdigital.usp.br/jupiterweb/autenticar")
    data = getPeriodoIdeal()
    textoResposta = "<b>Aluno:</b> "+data[0].get("nompes")+"\n"
    textoResposta += "<b>Curso:</b> "+data[0].get("nomcur")+"\n"
    textoResposta += "<b>Ano ingresso:</b> "+str(data[0].get("anoing"))+"\n\n"
    for periodo in data:
        textoResposta += "<b>"+periodo.get("periodo")+"</b>\n"
        textoResposta += "<b>Calculado em:</b> "+periodo.get("dtapcs")+"\n"
        if periodo.get("semidllcn") != "0":
            textoResposta += "<b>Período Ideal:</b> "+periodo.get("semidllcn")+"\n"
        elif periodo.get("semidlmtr") != "0":
            textoResposta += "<b>Período Ideal:</b> "+periodo.get("semidlmtr")+"º semestre\n"
        elif periodo.get("semidlqdm") != "0":
            textoResposta += "<b>Período Ideal:</b> "+periodo.get("semidlqdm")+"º quadrimestre\n"
        textoResposta += "<b>Média ponderada, considerando as reprovações:</b> "+str(periodo.get("medpon"))+"\n"
        textoResposta += "<b>Crédito acumulado:</b> "+str(periodo.get("totcrepgm"))+"\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=textoResposta, parse_mode=telegram.ParseMode.HTML)


historico_handler = CommandHandler('historico', historico)
acompCred_handler = CommandHandler('acompCred', acompCred)
periodoIdeal_handler = CommandHandler('periodoIdeal', periodoIdeal)
dispatcher.add_handler(historico_handler)
dispatcher.add_handler(acompCred_handler)
dispatcher.add_handler(periodoIdeal_handler)

updater.start_polling()

def getPeriodoIdeal():
    result = os.popen("curl 'https://uspdigital.usp.br/jupiterweb/dwr/call/plaincall/PeriodoIdealControleDWR.listarPeriodoIdeal.dwr' --data-raw 'callCount=1\nc0-scriptName=PeriodoIdealControleDWR\nc0-methodName=listarPeriodoIdeal\nc0-id=0\nc0-param0=string:"+os.environ.get('CODPES')+"\nbatchId=2\ninstanceId=0\npage=\nscriptSessionId=\n' -b cookies.txt").read()
    line = result.split("\n")[6]
    dataString = re.search("\[(.*?)\]", line).group()
    dataString = re.sub("(?<=:)(?!\s)", " ", dataString)
    data = yaml.load(dataString, yaml.SafeLoader)
    return data

def getHistorico():
    print("Obtendo histórico escolar")
    os.system("wget --save-cookies cookies.txt --keep-session-cookies --post-data 'codpes="+os.environ.get('CODPES')+"&senusu="+os.environ.get('SENUSU')+"&Submit+Entrar+&url=' --delete-after https://uspdigital.usp.br/jupiterweb/autenticar")
    os.system("wget --load-cookies cookies.txt -O HistoricoEscolar.pdf 'https://uspdigital.usp.br/jupiterweb/historicoescolarListar?cmd=cmd&codpgmclg=1%2FR%2F3&codcurhab=3032%2F3170%2FAtivo&opcclsturma=S'")

def getAcompCred():
    print("Obtendo total de créditos")
    os.system("wget --save-cookies cookies.txt --keep-session-cookies --post-data 'codpes="+os.environ.get('CODPES')+"&senusu="+os.environ.get('SENUSU')+"&Submit+Entrar+&url=' --delete-after https://uspdigital.usp.br/jupiterweb/autenticar")
    os.system("wget --load-cookies cookies.txt -O acompCred.png 'https://uspdigital.usp.br/jupiterweb/GraphicControle?tipografico=barGrupoDesempenho&codpgm=1&sequencia=0'")
