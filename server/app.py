#!/usr/bin/env python
from datetime import date
from importlib import import_module
import os
import re

# Flask / Webdienst
from flask import Flask, render_template, Response, send_from_directory, redirect
from flask.helpers import url_for, flash
import requests

from wtforms.fields.core import Label
from flask_cors import *
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message

# Forms
from forms import ChangeSammlerForm,ChangeSammlerMCP,YoloChangeSC,AlarmBenachrichtung

# import camera driver

from camera_opencv import Camera
import threading
from functionHelper import delete_file

import urs_config as cof

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

#FLASK API
app = Flask(__name__)
app.secret_key = 'ey0pX0EuIbB%wq4ey0pX0EuIbB%wq4ey0pX0EuIbB%wq4ey0pX0EuIbB%wq4'
#Flask Konfig
app.config['MAIL_SERVER']='smtp.1blu.de'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'b242501_0-marsrover'
app.config['MAIL_PASSWORD'] = 'tlMKzcehnrV)7Ed'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
bootstrap = Bootstrap(app)

CORS(app, supports_credentials=True)
camera = Camera()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/api/img/<path:filename>')
def sendimg(filename):
    return send_from_directory(dir_path+'/dist/img', filename)

@app.route('/js/<path:filename>')
def sendjs(filename):
    return send_from_directory(dir_path+'/dist/js', filename)

@app.route('/css/<path:filename>')
def sendcss(filename):
    return send_from_directory(dir_path+'/dist/css', filename)

@app.route('/api/img/icon/<path:filename>')
def sendicon(filename):
    return send_from_directory(dir_path+'/dist/img/icon', filename)

@app.route('/fonts/<path:filename>')
def sendfonts(filename):
    return send_from_directory(dir_path+'/dist/fonts', filename)

@app.route('/<path:filename>')
def sendgen(filename):
    return send_from_directory(dir_path+'/dist', filename)

@app.route('/')
def index():
    return send_from_directory(dir_path+'/dist', 'index.html')

# Dashboard
@app.route('/dashboard')
def dash():
    return render_template('index.html')

@app.route('/scanner/liste')
def sammler_liste():
    messages = []
    try:
        datei = open(cof.LIST_GEGEN,'r')
        for raw in datei:
            if not raw.startswith('----'):
                allmsg = raw.split(",")
                for entry in allmsg:
                    if len(entry) > 2:
                        messages.append(entry)
                    # Komplexität n^2
        datei.close()
    except FileNotFoundError:
        pass
    return render_template("Liste.html",messages=messages,neuladen=True)

@app.route('/api/foto')
def foto():
    return send_from_directory(dir_path,"pic.jpg")

@app.route('/change/sc/<name>', methods=['GET','POST'])
def change_sc(name):
    """ Generisches Single Choice Einstellung"""
    # Settings
    filename = ""
    title = ""

    # Modus herausfinden
    integer = -1
    try:
        integer = int(name)
    except ValueError:
        flash('Error: Wert nicht erkannt')
        return redirect(url_for('dash'))        

    if integer == 0:
        # Sammel Modus
        filename = cof.SAMMLER_CONF
        title = "Sammel Modus"
    elif integer == 1:
        # Alarm Modus
        filename = cof.ALARM_CONF
        title = "Alarm Modus"
    else:
        flash('Error: Modus nicht bekannt')
        return redirect(url_for('dash'))
    
    #Formular erstellen
    form = ChangeSammlerForm()
    
    # Einstellungen speichern
    if form.validate_on_submit():
        # Einstellungsdatei löschen
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        # Einstellungsdatei erstellen
        datei = open(filename,'a')
        zu_setzen = ""
        if form.textarea1.data != 'None':
            zu_setzen = zu_setzen + form.textarea1.data + ","
        if form.textarea2.data != 'None':
            zu_setzen = zu_setzen + form.textarea2.data + ","
        if form.textarea3.data != 'None':
            zu_setzen = zu_setzen + form.textarea3.data + ","
        if form.textarea4.data != 'None':
            zu_setzen = zu_setzen + form.textarea4.data + ","   
        
        # Letztes Komma abtrennen
        print("Original: "+zu_setzen)
        zu_setzen = zu_setzen[:-1]
        print("Cutted: "+ zu_setzen)

        # Einstellungsdatei schreiben
        datei.write(zu_setzen)
        datei.flush()
        datei.close()

        #GET-Request erfolgreich abgesetzt; bereit zum flashen
        flash('Erfolgreich auf: ' + zu_setzen + " gesetzt.")
        return redirect(url_for('change_sc',name=name))
    # Sammler Konfig laden 
    voreingestellt = ""
    try:
        datei = open(filename,'r')
        voreingestellt = datei.readline()
        datei.close()
    except FileNotFoundError:
        pass
    return render_template('quick_form.html',form=form,preset=voreingestellt,label=title+": Einstellungen")

@app.route('/change/mcp/<name>', methods=['GET','POST'])
def change_mcp(name):
    """ Generisches MCP Selection"""
    # Settings
    filename = ""
    title = ""
    
    # Modus herausfinden
    integer = -1
    try:
        integer = int(name)
    except ValueError:
        flash('Error: Eingabe nicht erkannt')
        return redirect(url_for('dash'))        

    if integer == 0:
        # Sammel Modus
        filename = cof.SAMMLER_CONF
        title = "Sammel Modus"
    elif integer == 1:
        # Alarm Modus
        filename = cof.ALARM_CONF
        title = "Alarm Modus"
    else:
        # Unbekannter Modus
        flash('Error: Modus nicht bekannt')
        return redirect(url_for('dash'))
    form = ChangeSammlerMCP()

    #Zum speichern der Daten
    if form.validate_on_submit():
        Arraystr = ""
        
        # Checkboxes Analysieren
        if form.btn1.data:
            Arraystr = Arraystr + 'person'+ "," 
        if form.btn2.data:
            Arraystr = Arraystr + 'umbrella' + "," 
        if form.btn3.data:
            Arraystr = Arraystr + 'handbag'+ "," 
        if form.btn4.data:
            Arraystr = Arraystr + 'bottle'+ "," 
        if form.btn5.data:
            Arraystr = Arraystr + 'wine glass'+ "," 
        if form.btn6.data:
            Arraystr = Arraystr + 'cup'+ "," 
        if form.btn7.data:
            Arraystr = Arraystr + 'fork'+ "," 
        if form.btn8.data:
            Arraystr = Arraystr + 'spoon'+ "," 
        if form.btn9.data:
            Arraystr = Arraystr + 'chair'+ "," 
        if form.btn10.data:
            Arraystr = Arraystr + 'mouse'+ "," 
        if form.btn11.data:
            Arraystr = Arraystr + 'book'+ "," 
        if form.btn12.data:
            Arraystr = Arraystr + 'vase'+ ","
        if form.btn13.data:
            Arraystr = Arraystr + 'laptop'+ ","
        
        # Einstellungsdatei löschen
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
        # Einstellungsdatei schreiben
        datei = open(filename,'a')

        # Letztes Komma abtrennen
        print("Original: "+Arraystr)
        Arraystr = Arraystr[:-1]
        print("Cutted: "+ Arraystr)
        datei.write(Arraystr)
        datei.flush()
        datei.close()

        flash('Erfolgreich auf: ' + Arraystr + " gesetzt.")
        return redirect(url_for('change_mcp',name=name))
    # Konfig Datei öffnen im Lese Modus
    # Zum zeigen, das es gepeichert wurden ist
    voreingestellt = ""
    try:
        datei = open(filename,'r')
        voreingestellt = datei.readline()
        datei.close()
    except FileNotFoundError:
        pass
    return render_template('quick_form.html',form=form,preset=voreingestellt,label=title+": Einstellungen")

# Mein Abschnitt mit meinen Funktionen
@app.route('/api/send/mail/<text>', methods=['GET','POST'])
def send_mail(text):
    empfanger = []
    try:
        datei_empfanger = open(cof.MAIL_EMP_CONF,"r")
        empfanger = datei_empfanger.readline().split(",")
        datei_empfanger.close()
        msg = Message('Mars Rover Alarm',sender='noreply@ursb.de',recipients=empfanger)
        msg.body = text
        msg.html = text
        mail.send(msg)
    except FileNotFoundError:
        return("[Error] keine Empfängerdatei gefunden.")
    return "OK!"

@app.route('/api/send/telegram/<text>', methods=['GET','POST'])
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
        return "[Error] kein Token bzw. Empfänger gefunden."
    return "OK!"


@app.route('/yolo/sc', methods=['GET','POST'])
def yolo_sc():
    """YOLO Select Eingabe"""
    form = YoloChangeSC()
    if form.validate_on_submit():
        try:
            os.remove(cof.YOLO_CONF)
        except FileNotFoundError:
            pass

        # Einstellungsdatei erstellen
        datei = open(cof.YOLO_CONF,'a')

        # Einstellungsdatei schreiben
        datei.write(form.textarea1.data)
        datei.flush()
        datei.close()

        flash('Erfolgreich auf: ' + form.textarea1.data + " gesetzt.")
        return redirect(url_for('yolo_sc'))
    voreingestellt = ""
    try:
        datei = open(cof.YOLO_CONF,'r')
        voreingestellt = datei.readline()
        datei.close()
    except FileNotFoundError:
        pass
    return render_template('quick_form.html',form=form,preset=voreingestellt,label="YOLO Modus 1+2: Sucheinstellungen")

# Alarm Modus 
# Benachrichtung
@app.route('/alarm/benachrichtung', methods=['GET','POST'])
def alarm_nach():
    form = AlarmBenachrichtung()
    if form.validate_on_submit():
        save_str = ""
        if form.mail_btn.data:
            save_str = save_str + "mail,"
        if form.tg_btn.data:
            save_str = save_str + "telegram,"

        # Alarm config schreiben
        delete_file(cof.ALARM_MSG_CONF)
        alarm = open(cof.ALARM_MSG_CONF,"a")
        alarm.write(save_str)
        alarm.flush()
        alarm.close()

        #Telegram config schreiben
        delete_file(cof.TELEGRAM_BOT_CONF)
        bot = open(cof.TELEGRAM_BOT_CONF,'a')
        bot.write(form.tg_bot.data)
        bot.flush()
        bot.close()

        # Telegram Empfänger config schreiben
        delete_file(cof.TELEGRAM_EMP_CONF)
        empfaenger = open(cof.TELEGRAM_EMP_CONF,'a')
        empfaenger.write(form.tg_user.data)
        empfaenger.flush()
        empfaenger.close()

        # E-Mail Empfänger schreiben
        delete_file(cof.MAIL_EMP_CONF)
        mail_emp = open(cof.MAIL_EMP_CONF,'a')
        mail_emp.write(form.mail_empfanger.data)
        mail_emp.flush()
        mail_emp.close()

        flash("Erfolgreich gespeichert!")
        return redirect(url_for('alarm_nach'))
     
    try:
        datei_alarm = open(cof.ALARM_MSG_CONF,"r")
        inhalt = datei_alarm.readline().split(",")
        if "mail" in inhalt:
            form.mail_btn.data = True
        if "telegram" in inhalt:
            form.tg_btn.data = True
        datei_alarm.close()
    except FileNotFoundError:
        flash("[Error] ALARM Conf")

    try:
        # Empfänger lesen und ins Formular eintragen
        datei_emp = open(cof.TELEGRAM_EMP_CONF,"r")
        form.tg_user.data = datei_emp.readline()
        datei_emp.close()
    except FileNotFoundError:
        flash("[Error] Telegram Empfänger ID Conf")

    try:
        # Bot token lesen
        datei_token = open(cof.TELEGRAM_BOT_CONF, "r")
        form.tg_bot.data = datei_token.readline()
        datei_token.close()
    except FileNotFoundError:
        flash("[Error] Bot Token Conf")

    return render_template('quick_form.html',form=form,label="Alarm Benachrichtungeinstellungen")


class webapp:
    def __init__(self):
        self.camera = camera

    def modeselect(self, modeInput):
        Camera.modeSelect = modeInput

    def colorFindSet(self, H, S, V):
        camera.colorFindSet(H, S, V)

    def thread(self):
        app.run(host='0.0.0.0', threaded=True)

    def startthread(self):
        fps_threading=threading.Thread(target=self.thread)         #Define a thread for FPV and OpenCV
        fps_threading.setDaemon(False)                             #'True' means it is a front thread,it would close when the mainloop() closes
        fps_threading.start()                                     #Thread starts
