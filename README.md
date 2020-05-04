# WTFormsValidator
A python library for generating client side validation functions from [WTForms](https://wtforms.readthedocs.io/) for various validator libraries.

Developed and tested with Python 3.8 and WTForms 2.3.1
Compatible with Python 3.6 and Python 3.7

## Supported validators

Here you can see which libraries are currently supported or planned to be added, and which WTForms validators are supported by them.  
Validators marked with an R are supported via regexes. Using multiple regex-backed validators concurrently will disable all but the last one.

| WTForms validator | [YairEO](https://github.com/yairEO/validator) | [ParsleyJS](https://parsleyjs.org/doc/examples.html)  | [Bouncer.js](https://github.com/cferdinandi/bouncer) | [just-validate](https://github.com/horprogs/Just-validate) | [Pristine](https://github.com/sha256/Pristine) | [jQuery validation](https://github.com/jquery-validation/jquery-validation) |
|-------------------|--------|-----------|------------|---------------|----------|-------------------|
| DataRequired      |  ✔️    |  ✔️        | TODO           |         TODO      | TODO         | TODO                  |
| Email             |✔️\|R¹|✔️\|R¹|            |               |          |                   |
| EqualTo           | ✔️     |  ✔️         |            |               |          |                   |
| InputRequired     | ✔️²     |  ✔️²         |            |               |          |                   |
| IPAddress         | R       | R          |            |               |          |                   |
| Length            | ✔️       |  ✔️         |            |               |          |                   |
| MacAddress        | R       |✔️            |            |               |          |                   |
| NumberRange       | ✔️       |  ✔️         |            |               |          |                   |
| Optional          | ✔️³  |  ✔️         |            |               |          |                   |
| Regexp            | ✔️       | ✔️          |            |               |          |                   |
| URL               |✔️\|R¹|✔️\|R¹|            |               |          |                   |
| UUID              | R       | R          |            |               |          |                   |
| AnyOf             | R       | R          |            |               |          |                   |
| NoneOf            | R       | R          |            |               |          |                   |
| Custom validators | ❌       | ❌          |            |               |          |                   |

¹ These libraries have built-in support for e-mail and URL validation, but you can choose to use the WTFormsValidation's regex validators instead. Defaults to built-in, unless that requires WTFormsValidation to change the field's type (in the case of YairEO)
² Same behaviour as DataRequired  
³ Due to a bug in YairEO, only fields marked as required are validated, so currently this should have no effect  

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
yaireo_tagger = YairEOtagger(email_builtin=True, url_builtin=True)  # defaults negated
...
render_template('your_template.html', form=yaireo_tagger.extend(form))
```

### Integrating with ParsleyJS

Using the default settings for the tagger class:
```
from WTFormsValidation import parslify
...
render_template('your_template.html', form=parslify(form))
```

or by instantiating the tagger class yourself:
```
from WTFormsValidation.tagging.parsley import ParsleyTagger
parsley_tagger = ParsleyTagger(email_builtin=False, url_builtin=False)  # defaults negated
...
render_template('your_template.html', form=parsley_tagger.extend(form))
```

