from flask_wtf import FlaskForm
from wtforms  import StringField, TextAreaField, DateTimeField, PasswordField
from wtforms.validators import DataRequired

class ExampleForm(FlaskForm):
	title = StringField(u'Título', validators = [DataRequired()])
	content = TextAreaField(u'Conteúdo')
	date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(FlaskForm):
	user = StringField(u'Usuário', validators = [DataRequired()])
	password = PasswordField(u'Senha', validators = [DataRequired()])
