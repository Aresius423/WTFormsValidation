"""Class for providing YairEO style tags"""

from typing import Dict

from wtforms.fields import Field
from wtforms import Form, validators

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

    def URLTags(self, validator: validators.URL):
        if self.url_builtin:
            return {'type': 'url'}
        else:
            return {'pattern': URL_REGEX}

    def DataRequiredTags(self, validator: validators.DataRequired):
        return {'required': ''}

    def InputRequiredTags(self, validator: validators.InputRequired):
        return {'required': ''}

    def EmailTags(self, validator: validators.Email):
        if self.email_builtin:
            return {'type': 'email'}
        else:
            return {'pattern': EMAIL_REGEX}

    def EqualToTags(self, validator: validators.EqualTo):
        return {'data-validate-linked': validator.fieldname}

    def IPAddressTags(self, validator: validators.Email):
        if validator.ipv4 and validator.ipv6:
            return {'pattern': IPV46_REGEX}
        elif validator.ipv4:
            return {'pattern': IPV4_REGEX}
        elif validator.ipv6:
            return {'pattern': IPV6_REGEX}

    def LengthTags(self, validator: validators.Length):
        if validator.max == -1:
            return {'data-validate-length-range': f'{validator.min}'}
        return {'data-validate-length-range': f'{validator.min},{validator.max}'}

    def MacAddressTags(self, validator: validators.MacAddress):
        return {'pattern': MAC_REGEX}

    def NumberRangeTags(self, validator: validators.NumberRange):
        return {'data-validate-minmax': f'{validator.min},{validator.max}'}

    def RegexpTags(self, validator: validators.Regexp):
        return {'pattern': validator.regex.pattern}

    def UUIDTags(self, validator: validators.Regexp):
        return {'pattern': UUID_REGEX}

    def AnyOfTags(self, validator: validators.AnyOf):
        return {'pattern': any_of_regex(validator.values)}

    def NoneOfTags(self, validator: validators.AnyOf):
        return {'pattern': none_of_regex(validator.values)}

    def OptionalTags(self, validator: validators.Optional):
        return {'optional': ''}
