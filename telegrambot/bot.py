from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import os

#import server.urs_config as cof
#from server.functionHelper import delete_file

#pip install python-telegram-bot

TELEGRAM_EMP_CONF = '/root/urs_robot/server/tg_empf.csv'
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
    try:
        # Datei lesen und verstehen
        datei = open(TELEGRAM_EMP_CONF,"r")
        line = datei.readline()
        line = line.replace("\n","")
        line = line.replace("\r","")
        array = line.split(",")
        datei.close()
        # ID des Telegram Nutzer herausfinden
        id = str(update.effective_user.id)
        print("Regsiterung von:",id,"...")

        if id not in array:
            # Registierung ist erfolgreich, weil er nicht in der Liste ist
            delete_file(TELEGRAM_EMP_CONF)
            datei = open(TELEGRAM_EMP_CONF,"a")
            datei.write(line+","+id)
            datei.flush()
            datei.close()
            update.message.reply_text(f'Du hast dich erfolgreich registiert. Du wirst zukünftig benachrichtig. Zum löschen dieser Registierung, gehe in Urs Dashboard unter der URL: /dashboard')
        else:
            # Registierung nicht erfolgreich, da er schon in der Liste ist
            update.message.reply_text(f'Du bist schon registiert.')
    except FileNotFoundError:
        print("FAIL")
        update.message.reply_text(f'Ich konnte dich leider nicht registiren, da Fehler passiert ist.')
    

updater = Updater('2050496929:AAHmHvQuPsPBqm4CqWj-QRPcGNksvk8BMDY')

updater.dispatcher.add_handler(CommandHandler('start', hello))
updater.dispatcher.add_handler(CommandHandler('id', id))
updater.dispatcher.add_handler(CommandHandler('register', register))

updater.start_polling()
updater.idle()