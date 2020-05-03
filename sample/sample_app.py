from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms import validators

from typing import Callable

from WTFormsValidation import yairify, parslify
from WTFormsValidation.tagging.yaireo import YairEOtagger
from WTFormsValidation.tagging.parsley import ParsleyTagger

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)


class ExampleForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # YairEO requires us to set everything to Required
        # see: https://github.com/yairEO/validator/issues/63
        for field in self:
            field.validators += (validators.DataRequired(),)

    def add_parsley_listeners(self):
        for field in self:
            if field.render_kw is None:
                field.render_kw = {'data-parsley-trigger': 'focusout'}
            else:
                field.render_kw.update({'data-parsley-trigger': 'focusout'})

    name = StringField('Name')
    email = StringField('E-mail address', validators=[validators.Email()])
    date = StringField('Date in yyyy-mm-dd format', validators=[validators.Regexp(r'\d{4}-\d{2}-\d{2}')])
    nameCheck = StringField('Equal to the name field', validators=[validators.EqualTo('name')])
    ipv4 = StringField('Valid IPv4 address', validators=[validators.IPAddress(ipv4=True, ipv6=False)])
    ipv6 = StringField('Valid IPv6 address', validators=[validators.IPAddress(ipv4=False, ipv6=True)])
    ipv46 = StringField('Valid IPv4 or IPv6 address', validators=[validators.IPAddress(ipv4=True, ipv6=True)])
    length_range = StringField('3-8 chars long string', validators=[validators.Length(3, 8)])
    length_range_2 = StringField('min. 3 chars long string', validators=[validators.Length(min=3)])
    mac = StringField('MAC address', validators=[validators.MacAddress()])

    # YairEO requires type to be number
    num_range = StringField('Number between 3 and 8', validators=[validators.NumberRange(3, 8)], render_kw={'type': 'number'})
    num_range_2 = StringField('Number above 2', validators=[validators.NumberRange(min=3)], render_kw={'type': 'number'})

    url = StringField('Valid URL', validators=[validators.URL()])
    uuid = StringField('UUID', validators=[validators.UUID()])

    anyof = StringField('Strings alice or [bob]', validators=[validators.AnyOf(['alice', '[bob]'])])
    noneof = StringField('Strings NOT alice or [bob]', validators=[validators.NoneOf(['alice', '[bob]'])])


def render_page(template: str, form: FlaskForm, **kwargs):
    return render_template(template, message='Test page', form=form, **kwargs)


def colour_text(text: str, colour: str) -> str:
    return f'<p style="color:{colour}">{text}</p>'


@app.route('/', methods=['GET', 'POST'])
def no_validator():
    form = ExampleForm()
    return make_page('index.html', form)


@app.route('/yaireo', methods=['GET', 'POST'])
def yaireo_builtin():
    form = ExampleForm()
    return make_page('yaireo.html', yairify(form))


@app.route('/yaireo_builtin', methods=['GET', 'POST'])
def yaireo():
    tagger = YairEOtagger(email_builtin=True, url_builtin=True)
    form = ExampleForm()
    return make_page('yaireo.html', tagger.extend(form))


@app.route('/parsley_builtin', methods=['GET', 'POST'])
def parsley_builtin():
    form = ExampleForm()
    form.add_parsley_listeners()
    return make_page('parsley.html', parslify(form))


@app.route('/parsley_regex', methods=['GET', 'POST'])
def parsley_regex():
    tagger = ParsleyTagger(email_builtin=False, url_builtin=False)
    form = ExampleForm()
    form.add_parsley_listeners()
    return make_page('parsley.html', tagger.extend(form))


def make_page(template, form: FlaskForm):
    if request.method == 'POST':
        if form.validate():
            return render_page(template, form, result=colour_text('Form passed backend validation', 'green'))
        return render_page(template, form, result=colour_text('Form failed backend validation', 'red'), log=form.errors)
    return render_page(template, form)


if __name__ == '__main__':
    app.secret_key = 'correcthorsebatterystaple'
    app.run(debug=True)
