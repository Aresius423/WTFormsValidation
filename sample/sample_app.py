from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms import validators

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)


class ExampleForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = EmailField('E-mail address', validators=[validators.DataRequired(), validators.Email()])
    date = StringField('A date in yyyy-mm-dd format', validators=[validators.Regexp(r'\d{4}-\d{2}-\d{2}')])


def render_index(form: FlaskForm, **kwargs):
    return render_template('index.html', message='Test page', form=form, **kwargs)


def colour_text(text: str, colour: str) -> str:
    return f'<p style="color:{colour}">{text}</p>'


@app.route('/', methods=['GET', 'POST'])
def index_get():
    form = ExampleForm()
    if request.method == 'POST':
        if form.validate():
            return render_index(form, result=colour_text('Form passed backend validation', 'green'))
        return render_index(form, result=colour_text('Form failed backend validation', 'red'), log=form.errors)
    return render_index(form)


if __name__ == '__main__':
    app.secret_key = 'correcthorsebatterystaple'
    app.run(debug=True)
