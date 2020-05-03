# WTFormsValidator
A python library for generating client side validation functions from [WTForms](https://wtforms.readthedocs.io/) for various validator libraries.

Developed and tested with Python 3.8 and WTForms 2.3.1
Compatible with Python 3.6 and Python 3.7

## Supported validators

Here you can see which libraries are currently supported or planned to be added, and which WTForms validators are supported by them.  
Validators marked with an R are supported via regexes. Using multiple regex-backed validators concurrently will disable all but the last one.

| WTForms validator | [YairEO](https://github.com/yairEO/validator) | [ParsleyJS](https://parsleyjs.org/doc/examples.html)  | [Bouncer.js](https://github.com/cferdinandi/bouncer) | [just-validate](https://github.com/horprogs/Just-validate) | [Pristine](https://github.com/sha256/Pristine) | [jQuery validation](https://github.com/jquery-validation/jquery-validation) |
|-------------------|--------|-----------|------------|---------------|----------|-------------------|
| DataRequired      |  ✔️    |  TODO         | TODO           |         TODO      | TODO         | TODO                  |
| Email             | ✔️ \| R ¹|          |            |               |          |                   |
| EqualTo           | ✔️     |           |            |               |          |                   |
| InputRequired     | ✔️ ³    |           |            |               |          |                   |
| IPAddress         | R       |           |            |               |          |                   |
| Length            | ✔️       |           |            |               |          |                   |
| MacAddress        | R       |           |            |               |          |                   |
| NumberRange       | ✔️ ²       |           |            |               |          |                   |
| Optional          | ✔️ ⁴ |           |            |               |          |                   |
| Regexp            | ✔️       |           |            |               |          |                   |
| URL               | ✔️ \| R *|           |            |               |          |                   |
| UUID              | R       |           |            |               |          |                   |
| AnyOf             | R       |           |            |               |          |                   |
| NoneOf            | R       |           |            |               |          |                   |
| Custom validators | ❌       |           |            |               |          |                   |

¹ YairEO has built-in support for e-mail and URL validation, however these require the input field's type to be set to "email" and "url" respectively. By default, the regex-backed validator is used, but you can choose to use the built-in validators by instantiating YairEOtagger yourself.
² To use this validator, you have to set the input field's type to "number"
³ Same behaviour as DataRequired
⁴ Due to a bug in YairEO, only fields marked as required are validated, so currently this should have no effect

## Running the sample application

* Create a virtualenv ```virtualenv -p python3.8 venv```
* Activate it ```. venv/bin/activate```
* Install the sample's requirements ```pip install -r sample/requirements.txt```
* run ```python -m sample.sample_app```

GET ```localhost:5000``` → only backend and on-the-fly default HTML5 validation
GET ```localhost:5000/yaireo``` → YairEO on-the-fly validation
GET ```localhost:5000/yaireo``` → YairEO on-the-fly validation with built-in URL and e-mail validator
## Usage

Adding the validator library's boilerplate code should be done according to their documentation. Integrate WTFormsValidator as described below.

### Integrating with YairEO

Using the default settings for the tagger class:
```
from WTFormsValidation import yairify
...
render_template('your_template.html', form=yairify(form))
```

or by instantiating the tagger class yourself:
```
from WTFormsValidation.tagging.yaireo import YairEOtagger
yaireo_tagger = YairEOtagger(email_builtin=True, url_builtin=True)
...
render_template('your_template.html', form=yaireo_tagger.extend(form))
```

