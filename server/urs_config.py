import base64

URL = 'http://192.168.1.103:5000'
"""URL für dem Objekterkennungs Server"""
#URL = 'http://localhost:5000'
PIC_PATH = '/root/urs_robot/server/pic.jpg'
"""Pfad, wo wir das Foto abgreifen können"""

URL_OPTION = '/send-image/data:image/jpeg;base64,'
"""Wie wurde das Bild kodiert, inklusiv URL"""

LIST_GEGEN = 'gegenstaende.csv'
""" Auflistung der gefunden Gegenstände"""

SAMMLER_CONF = 'sammler.csv'
""" Auflsitungen der zu suchenden Objekte"""

ALARM_CONF = 'alarm.csv'
""" Bei welchen Objekt soll der Roboter alarm schlagen"""

ALARM_MSG_CONF = 'alarmnachricht.csv'


YOLO_CONF = 'yolo.csv'
""" YOLO Such und fahr hin Gegenstand"""



ROBOT_SPEED = 95
""" Geschwindigkeit des Roboter"""

TELEGRAM_EMPFANGER = "978618750"
TELEGRAM_BOT_TOKEN = "1233498807:AAGpVIwJMwxTvzcaMJmEog1NmN7XZZYlTDk"
TELEGRAM_BOT_URL = "https://api.telegram.org/bot"+TELEGRAM_BOT_TOKEN+"/sendMessage?chat_id="+TELEGRAM_EMPFANGER+"&text="

def get_base64_encoded_image(image_path):
    """Bild -> Base64 String"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

