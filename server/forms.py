from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextField

class ChangeSammlerForm(FlaskForm):
    dropdown_list = ['None','person','umbrella','handbag','bottle','wine glass','cup','fork','knife','spoon','chair','mouse','book','vase','laptop']
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
    btn8 = BooleanField('spoon')
    btn9 = BooleanField('chair')
    btn10 = BooleanField('mouse')
    btn11 = BooleanField('book')
    btn12 = BooleanField('vase')
    btn13 = BooleanField('laptop')
    submit = SubmitField('Speichern')

class YoloChangeSC(FlaskForm):
    dropdown_list = ['None','person','umbrella','handbag','bottle','wine glass','cup','fork','knife','spoon','chair','mouse','book','vase']
    textarea1 = SelectField('Gegenstand 1',choices=dropdown_list, default=1)
    submit = SubmitField('Speichern')

class AlarmBenachrichtung(FlaskForm):
    mail_btn = BooleanField('E-Mail Benachrichtung')
    tg_btn = BooleanField('Telegram Benachrichtung')
    tg_user = TextField('Telegram User ID')
    tg_bot = TextField('Telegram Bot Token')
    submit = SubmitField('Speichern')
