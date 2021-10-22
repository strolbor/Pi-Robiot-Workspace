import urs_config as cof
import requests


def send_telegram(text):
    try:
        datei_empfanger = open(cof.TELEGRAM_EMP_CONF,"r")
        empfanger = datei_empfanger.readline().split(",")
        datei_empfanger.close()
        datei_token = open(cof.TELEGRAM_BOT_CONF,"r")
        token = datei_token.readline()
        for entry in empfanger:
            requests.post(cof.TELEGRAM_BOT_URL_0+token+cof.TELEGRAM_BOT_URL_1+entry+cof.TELEGRAM_BOT_URL_2+text)
    except FileNotFoundError:
        pass