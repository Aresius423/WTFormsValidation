"""Class for providing YairEO style tags"""

from typing import Dict

from wtforms.fields import Field
from wtforms import validators

from WTFormsValidation.tagging.base import TaggerBase
from WTFormsValidation.regex_utils import EMAIL_REGEX, IPV4_REGEX, IPV6_REGEX, \
        IPV46_REGEX, MAC_REGEX, URL_REGEX, UUID_REGEX, any_of_regex, none_of_regex


class YairEOtagger(TaggerBase):
    """Class for providing YairEO style tags"""
    def __init__(self, email_builtin=False, url_builtin=False):
        """Constructor for the class.

        @param email_builtin: Setting this will use YairEO's e-mail validator, but will set type="email" on the field
        @param url_builtin: Setting this will use YairEO's URL validator, but will set type="email" on the field
        """
        self.email_builtin = email_builtin
        self.url_builtin = url_builtin

    def tags(self, field: Field) -> Dict:
        result = dict()
        for validator in field.validators:
            result.update(self.validator_to_dict(validator))

        return result

    def validator_to_dict(self, validator) -> Dict:  # mypy: ignore

        if hasattr(validator, 'validate_hostname'):
            # URL validator is really just a regex in disguise
            if self.url_builtin:
                return {'type': 'url'}
            else:
                return {'pattern': URL_REGEX}
        if isinstance(validator, validators.DataRequired):
            return {'required': ''}

        if isinstance(validator, validators.InputRequired):
            return {'required': ''}

        elif isinstance(validator, validators.Email):
            if self.email_builtin:
                return {'type': 'email'}
            else:
                return {'pattern': EMAIL_REGEX}

        elif isinstance(validator, validators.EqualTo):
            return {'data-validate-linked': validator.fieldname}

        elif isinstance(validator, validators.IPAddress):
            if validator.ipv4 and validator.ipv6:
                return {'pattern': IPV46_REGEX}
            elif validator.ipv4:
                return {'pattern': IPV4_REGEX}
            elif validator.ipv6:
                return {'pattern': IPV6_REGEX}

        elif isinstance(validator, validators.Length):
            return {'data-validate-length-range': f'{validator.min},{validator.max}'}

        elif isinstance(validator, validators.MacAddress):
            return {'pattern': MAC_REGEX}

        elif isinstance(validator, validators.NumberRange):
            return {'data-validate-minmax': f'{validator.min},{validator.max}'}

        elif isinstance(validator, validators.Regexp):
            return {'pattern': validator.regex.pattern}

        elif isinstance(validator, validators.UUID):
            return {'pattern': UUID_REGEX}

        elif isinstance(validator, validators.AnyOf):
            return {'pattern': any_of_regex(validator.values)}

        elif isinstance(validator, validators.NoneOf):
            return {'pattern': none_of_regex(validator.values)}

        elif isinstance(validator, validators.Optional):
            return {'optional': ''}

        # Unknown validators we can't deal with
        return {}
