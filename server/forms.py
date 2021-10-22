from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField, TextField
from wtforms.validators import DataRequired

dropdown_list = ['None','person','umbrella','handbag','bottle','wine glass','cup','fork','knife','spoon','chair','mouse','book','vase','laptop']

class ChangeSammlerForm(FlaskForm):
    textarea1= SelectField('Gegenstand 1', choices=dropdown_list, default=1)
    textarea2= SelectField('Gegenstand 2', choices=dropdown_list, default=1)
    textarea3= SelectField('Gegenstand 3', choices=dropdown_list, default=1)
    textarea4= SelectField('Gegenstand 4', choices=dropdown_list, default=1)
    submit = SubmitField('Speichern')

class ChangeSammlerMCP(FlaskForm):
    btn1 = BooleanField('person')
    btn2 = BooleanField('umbrella')
    btn3 = BooleanField('handbag')
    btn4 = BooleanField('bottle')
    btn5 = BooleanField('wine glass')
    btn6 = BooleanField('cup')
    btn7 = BooleanField('fork')
    btn7a = BooleanField('knife')
    btn8 = BooleanField('spoon')
    btn9 = BooleanField('chair')
    btn10 = BooleanField('mouse')
    btn11 = BooleanField('book')
    btn12 = BooleanField('vase')
    btn13 = BooleanField('laptop')
    submit = SubmitField('Speichern')

class YoloChangeSC(FlaskForm):
    textarea1 = SelectField('Gegenstand 1',choices=dropdown_list, default=1)
    submit = SubmitField('Speichern')

class AlarmBenachrichtung(FlaskForm):
    mail_btn = BooleanField('E-Mail Benachrichtung')
    tg_btn = BooleanField('Telegram Benachrichtung')
    mail_empfanger = TextField('E-Mail Empfänger (getrennt mit ,)')
    tg_user = TextField('Telegram Empfänger ID (getrennt mit ,)')
    tg_bot = PasswordField('Telegram Bot Token')
    submit = SubmitField('Speichern')

class EmailChange(FlaskForm):
    server = TextField('E-Mail Server',validators=[DataRequired()])
    port = TextField('Port',validators=[DataRequired()])
    username = TextField('Username',validators=[DataRequired()])
    password = PasswordField('Passwort',validators=[DataRequired()])
    submit = SubmitField('Speichern')