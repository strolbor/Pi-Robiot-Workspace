from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import os

#import server.urs_config as cof
#from server.functionHelper import delete_file

#pip install python-telegram-bot

TELEGRAM_EMP_CONF = '/root/urs_robot/server/tg_empf.csv'
#TELEGRAM_EMP_CONF = 'a.tmp'
"""Hier wird die ID des Empfängers der Nachricht hinterlegt."""

def delete_file(filename):
	"""Datei löschen"""
	if os.path.exists(filename): # Wenn Datei vorhanden
		os.remove(filename) # Lösche diese Datei


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hallo {update.effective_user.first_name}! '+
    'Falls du Kontaktiert werden willst, rufe /id auf und notiere deine IP im Urs Dashboard unter Alarmeinstellungen.')

def id(update: Update, context: CallbackContext) -> None:
    id = update.effective_user.id
    print(id)
    update.message.reply_text(f'Deine ID ist: {id}')

def register(update: Update, context: CallbackContext) -> None:
    line = ""
    try:
        # Datei lesen und verstehen
        datei = open(TELEGRAM_EMP_CONF,"r")
        line = datei.readline()
        line = line.replace("\n","")
        line = line.replace("\r","")
        datei.close()
        print(line)
        # ID des Telegram Nutzer herausfinden
    except FileNotFoundError:
        pass

    id = str(update.effective_user.id)
    array = line.split(",")
    print("Registerung von:",id,"...")
    if id not in array:
        # Registierung ist erfolgreich, weil er nicht in der Liste ist
        delete_file(TELEGRAM_EMP_CONF)
        datei = open(TELEGRAM_EMP_CONF,"a")
        if len(line) == 0:
            datei.write(id)
        else:
            datei.write(line+","+id)
        datei.flush()
        datei.close()
        update.message.reply_text(f'Du hast dich erfolgreich registiert. Du wirst zukünftig benachrichtig. Zum löschen dieser Registierung, gehe in Urs Dashboard unter der URL: /dashboard')
        print("Erfolgreich")
    else:
       # Registierung nicht erfolgreich, da er schon in der Liste ist
        update.message.reply_text(f'Du bist schon registiert.')
        print("nicht erfolgreich")
    
def unregister(update: Update, context: CallbackContext) -> None:
    line = ""
    try:
        # Datei lesen und verstehen
        datei = open(TELEGRAM_EMP_CONF,"r")
        line = datei.readline()
        line = line.replace("\n","")
        line = line.replace("\r","")
        datei.close()
        print(line)
        # ID des Telegram Nutzer herausfinden
    except FileNotFoundError:
        pass

    id = str(update.effective_user.id)
    array = line.split(",")
    print("Unregisterung von:",id,"...")
    print(array)
    if id in array:
        new_line = ""
        for entry in array:
            if entry != id:
                new_line = new_line + entry + "," 
        delete_file(TELEGRAM_EMP_CONF)
        datei = open(TELEGRAM_EMP_CONF,"a")
        datei.write(new_line)
        datei.flush()
        datei.close()
        update.message.reply_text(f'Du hast dich erfolgreich unregistiert.')
        print("Erfolgreich")
    else:
       # Registierung nicht erfolgreich, da er schon in der Liste ist
        update.message.reply_text(f'Du bist gar nicht registiert. Also ist nichts zu machen')
        print("nicht erfolgreich")
    

updater = Updater('2050496929:AAHmHvQuPsPBqm4CqWj-QRPcGNksvk8BMDY')

updater.dispatcher.add_handler(CommandHandler('start', hello))
updater.dispatcher.add_handler(CommandHandler('id', id))
updater.dispatcher.add_handler(CommandHandler('register', register))
updater.dispatcher.add_handler(CommandHandler('unregister', unregister))

updater.start_polling()
updater.idle()