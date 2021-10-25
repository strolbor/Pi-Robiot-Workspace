#!/usr/bin/env python
import os
import re

# Flask / Webdienst
from flask import Flask, render_template, Response, send_from_directory, redirect
from flask.helpers import url_for, flash
from flask.wrappers import Request
from numpy import array
from werkzeug.wrappers import request as werkzeug_request

from flask_cors import *
from flask_bootstrap import Bootstrap
from flask_mail import Mail

# Forms
from forms import *


# import camera driver

from camera_opencv import Camera
import threading
from functionHelper import delete_file

import urs_config as cof
import constant as c
import sendHelper as sdH

QUICK_FORM = 'quick_form.html'
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

#FLASK API
app = Flask(__name__)
app.secret_key = 'ey0pX0EuIbB%wq4ey0pX0EuIbB%wq4ey0pX0EuIbB%wq4ey0pX0EuIbB%wq4'
#Flask Konfig
try:
    datei_mail = open(cof.MAIL_conf,"r")
    array = datei_mail.readline().split(",")
    #Eingabe Reihnfolge: Server,Port,Username,Passwort
    app.config['MAIL_SERVER']= array[0] #'smtp.1blu.de'
    app.config['MAIL_PORT'] = array[1] #587
    app.config['MAIL_USERNAME'] = array[2] #'b242501_0-marsrover'
    app.config['MAIL_PASSWORD'] = array[3] #'tlMKzcehnrV)7Ed'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
except FileNotFoundError:
    pass

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
        flash(c.FILE_NOT_FOUND_MSG)
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
        flash(c.INPUT_ERROR)
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
        flash(c.MODI_NOT_FOUND)
        return redirect(url_for('dash'))
    
    #Formular erstellen
    form = ChangeSammlerForm()
    
    # Einstellungen speichern
    if form.validate_on_submit():
        # Einstellungsdatei löschen
        delete_file(filename)
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
        flash(c.sucess_msg(zu_setzen))
        return redirect(url_for('change_sc',name=name))

    # Sammler Konfig laden 
    voreingestellt = ""
    try:
        datei = open(filename,'r')
        voreingestellt = datei.readline()
        datei.close()
        array = voreingestellt.split(",")
        anz_entry = len(array)
        if 0 < anz_entry:
            form.textarea1.data = array[0]
        if 1 < anz_entry:
            form.textarea2.data = array[1]
        if 2 < anz_entry:
            form.textarea3.data = array[2]
        if 3 < anz_entry:
            form.textarea4.data = array[3]
        
    except FileNotFoundError:
        pass
    return render_template(QUICK_FORM,form=form,label=title+": Einstellungen")

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
        # Eingabe nicht erkannt
        flash(c.INPUT_ERROR)
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
        flash(c.MODI_NOT_FOUND)
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
        if form.btn7a.data:
            Arraystr = Arraystr + 'knife'+ "," 
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
        delete_file(filename)
        # Einstellungsdatei schreiben
        datei = open(filename,'a')

        # Letztes Komma abtrennen
        print("Original: "+Arraystr)
        Arraystr = Arraystr[:-1]
        print("Cutted: "+ Arraystr)
        datei.write(Arraystr)
        datei.flush()
        datei.close()

        flash(c.sucess_msg(Arraystr))
        return redirect(url_for('change_mcp',name=name))
    # Konfig Datei öffnen im Lese Modus
    # Zum zeigen, das es gepeichert wurden ist
    voreingestellt = ""
    try:
        datei = open(filename,'r')
        voreingestellt = datei.readline()
        datei.close()
        array = voreingestellt.split(",")
        
        if 'person' in array:
            form.btn1.data = True
        if 'umbrella' in array:
            form.btn2.data = True
        if 'handbag' in array:
            form.btn3.data = True
        if 'bottle' in array:
            form.btn4.data = True
        if 'wine glass' in array:
            form.btn5.data = True
        if 'cup' in array:
            form.btn6.data = True
        if 'fork' in array:
            form.btn7.data = True
        if 'knife' in array:
            form.btn7a.data = True
        if 'spoon' in array:
            form.btn8.data = True
        if 'chair' in array:
            form.btn9.data = True
        if 'mouse' in array:
            form.btn10.data = True
        if 'book' in array:
            form.btn11.data = True
        if 'vase' in array:
            form.btn12.data = True
        if 'laptop' in array:
            form.btn13.data = True
        
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(filename))
    return render_template(QUICK_FORM,form=form,label=title+": Einstellungen")

# Mein Abschnitt mit meinen Funktionen


@app.route('/api/sendinfo/<text>')
def send_info(text):
    msg = []
    try:
        datei = open(cof.ALARM_MSG_CONF,'r')
        msg = datei.readline().split(",")
    except FileNotFoundError:
        return c.FILE_NOT_FOUND_MSG2.format(cof.ALARM_MSG_CONF)
    print('[API] Send Info')
    if "mail" in msg:
        sdH.send_mail(text,mail)
    if "telegram" in msg:
        sdH.send_telegram(text)
    print("[ALARM] Nachricht gesendet:",text)
    return "OK!"


@app.route('/yolo/sc', methods=['GET','POST'])
def yolo_sc():
    """YOLO Select Eingabe"""
    form = YoloChangeSC()
    if form.validate_on_submit():
        delete_file(cof.YOLO_CONF)
        # Einstellungsdatei erstellen
        datei = open(cof.YOLO_CONF,'a')

        # Einstellungsdatei schreiben
        datei.write(form.textarea1.data)
        datei.flush()
        datei.close()

        flash(c.sucess_msg(form.textarea1.data))
        return redirect(url_for('yolo_sc'))

    # Datei laden, sodass der Eintrag aktuell ist
    try:
        datei = open(cof.YOLO_CONF,'r')
        form.textarea1.data = datei.readline()
        datei.close()
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.YOLO_CONF))
    return render_template(QUICK_FORM,form=form,label="YOLO Modus 1+2: Sucheinstellungen")
    

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

        flash(c.SUCESS_MSG)
        return redirect(url_for('alarm_nach'))
     
    try: 
        # Radio Buttons Konfig einstellen
        datei_alarm = open(cof.ALARM_MSG_CONF,"r")
        inhalt = datei_alarm.readline().split(",")
        if "mail" in inhalt:
            form.mail_btn.data = True
        if "telegram" in inhalt:
            form.tg_btn.data = True
        datei_alarm.close()
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.ALARM_MSG_CONF))

    try:
        # Telegram Empfänger lesen und ins Formular eintragen
        datei_emp = open(cof.TELEGRAM_EMP_CONF,"r")
        form.tg_user.data = datei_emp.readline()
        datei_emp.close()
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.TELEGRAM_BOT_CONF))

    try:
        #E-Mail Empfänger lesen uns ins Formular eintragen
        datei_mail_emp = open(cof.MAIL_EMP_CONF,"r")
        form.mail_empfanger.data = datei_mail_emp.readline()
        datei_mail_emp.close()
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.MAIL_EMP_CONF))

    try:
        # Bot token lesen
        datei_token = open(cof.TELEGRAM_BOT_CONF, "r")
        form.tg_bot.data = datei_token.readline()
        datei_token.close()
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.TELEGRAM_BOT_CONF))

    return render_template(QUICK_FORM,form=form,label="Alarm Benachrichtungeinstellungen")

@app.route('/api/email', methods=['GET','POST'])
def email_cnf():
    """E-Mail Konfiguration"""
    #Eingabe Reihnfolge: Server,Port,Username,Passwort
    form = EmailChange()
    if form.validate_on_submit():
        delete_file(cof.MAIL_conf)
        datei = open(cof.MAIL_conf,"a")
        datei.write(form.server.data + "," + form.port.data + "," + form.username.data + "," + form.password.data + ",")
        datei.flush()
        datei.close()
        flash(c.SUCESS_MSG)
        return redirect(url_for('email_cnf'))
    #Konfig lesen
    try:
        datei = open(cof.MAIL_conf,"r")
        array = datei.readline().split(",")
        form.server.data = array[0]
        form.port.data = array[1]
        form.username.data = array[2]
        form.password.data = array[3] 
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.MAIL_conf))
    return render_template(QUICK_FORM,form=form,label="E-Mail Konfiguration")

@app.route('/api/untergrund',methods=['GET','POST'])
def untergrundsetting():
    form = UntergrundSetting()
    if form.validate_on_submit():
        delete_file(cof.ZEITFAKTOR)
        datei = open(cof.ZEITFAKTOR,"a")
        datei.write(str(form.eingabe.data)+",")
        datei.flush()
        datei.close()
        flash(c.SUCESS_MSG)
        return redirect(url_for('untergrundsetting'))
    #Konfig lesen
    try:
        datei = open(cof.ZEITFAKTOR,"r")
        form.eingabe.data = datei.readline().split(",")[0]
        datei.close()
    except FileNotFoundError:
        flash(c.FILE_NOT_FOUND_MSG2.format(cof.ZEITFAKTOR))
    info ="Dies wird verwendet, um die Drehgeschwindigkeit in einer Kurve zu modifizieren.\r\n" + \
    "Der Faktor 2 ist gleich zusetzen, wenn der Untergrund ein Teppich ist."
    return render_template(QUICK_FORM,form=form,label="Zeitfaktor modifizieren",info=info)


choices_array = []
@app.route('/api/Felder/<name>',methods=['GET','POST'])
def swip_swap(name):
    global choices_array
    form = d_felder()

    # Settings
    filename = ""
    title = ""
    
    # Modus herausfinden
    integer = -1
    try:
        integer = int(name)
    except ValueError:
        flash(c.INPUT_ERROR)
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
        flash(c.MODI_NOT_FOUND)
        return redirect(url_for('dash'))

    # Konfig Datei öffnen im Lese Modus
    # Zum zeigen, das es gepeichert wurden ist
    if form.submit.data == False and form.submit2.data == False and form.submit3.data == False:
        print("Erster Aufruf")
        try:
            choices_array = []
            datei = open(filename,'r')
            voreingestellt = datei.readline()
            datei.close()
            for entry in voreingestellt.split(","):
                choices_array.append([entry,entry])
            
        except FileNotFoundError:
            flash(c.FILE_NOT_FOUND_MSG2.format(filename))
    
    form.selected.choices = choices_array.copy()
    if form.validate_on_submit():
        print("Verfügbar:",form.ein.data)
        print("Eingestellt:",form.selected.data)
        print("0",form.submit.data) # Speichern
        print("1",form.submit2.data) # Hinzufügen
        print("2",form.submit3.data) # Entfernen
        if form.submit.data:
            # Dateien löschen und öffnen
            delete_file(filename)
            datei = open(filename,"a")

            #Daten herausfinden
            save_str = ""
            for entry in form.selected.choices.copy():
                save_str = save_str + "," + entry[0]
            save_str = save_str[1:]
            print(save_str)

            # Datei schreiben
            datei.write(save_str)
            datei.flush()
            datei.close()
            
            # Fertig gesetzt
            flash(c.SUCESS_MSG)
            return redirect(url_for('swip_swap',name=name))

        if form.submit2.data:
            # Item soll hinzugefügt werden

            # Choices werden hart kopiert
            old_choices = form.selected.choices.copy()

            # Neue ausgewählte Elemente werden kopiert
            # und hinzugefügt
            for entry in form.ein.data.copy():
                old_choices.append([entry,entry])
            # Neue List wird kopiert in die Liste
            form.selected.choices = old_choices.copy()
            choices_array = old_choices.copy()
            flash(c.SUC_ADD)
            return render_template("Listenfelder.html",form=form,label=title+": Einstellungen")
            #return redirect(url_for('swip_swap',name=name))
        if form.submit3.data:
            flash("Submit 3")
        flash("A")
        return redirect(url_for('swip_swap',name=name))

    return render_template("Listenfelder.html",form=form,label=title+": Einstellungen")#,label="label")
    #return render_template(QUICK_FORM,form=form)

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
