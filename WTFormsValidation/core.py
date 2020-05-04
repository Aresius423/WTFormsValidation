"""Core class to hold all converters"""

from typing import Dict, Type

from wtforms import Form
from WTFormsValidation.default_provider import default_provider


def yairify(form: Form) -> Form:
    """Add YairEO style validation tags to the provided form.
    See https://www.github.com/yairEO/validator for more info.

    @param form: the input WTForm
    @return: the form, with validator tags applied
    """
    return default_provider.yaireo().extend(form)


def parslify(form: Form) -> Form:
    """Add ParsleyJS style validation tags to the provided form.
    See https://www.parsleyjs.org for more info.

    @param form: the input WTForm
    @return: the form, with validator tags applied
    """
    return default_provider.parsley().extend(form)


def bouncify(form: Form, in_place: bool = False) -> Form:
    """Add Bounce.js style validation tags to the provided form.
    See https://www.bouncejs.com for more info.

    @param form: the input WTForm
    @return: the form, with validator tags applied
    """
    return default_provider.bouncer().extend(form)


def justvalidate():
    raise NotImplementedError


def pristinify():
    raise NotImplementedError


def jqvalidate():
    raise NotImplementedError
