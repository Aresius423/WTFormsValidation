"""Class for providing YairEO style tags"""

from typing import Dict

from wtforms.fields import Field
from wtforms import validators

from WTFormsValidation.tagging.base import TaggerBase
from WTFormsValidation.regex_utils import EMAIL_REGEX, IPV4_REGEX, IPV6_REGEX, \
        IPV46_REGEX, MAC_REGEX, URL_REGEX, UUID_REGEX, any_of_regex, none_of_regex


class ParsleyTagger(TaggerBase):
    """Class for providing ParsleyJS style tags"""
    def __init__(self, email_builtin=True, url_builtin=True):
        """Constructor for the class.

        @param email_builtin: Setting this will use Parsley's e-mail validator, but will set type="email" on the field
        @param url_builtin: Setting this will use Parsley's URL validator, but will set type="email" on the field
        """
        self.email_builtin = email_builtin
        self.url_builtin = url_builtin

    def tags(self, field: Field) -> Dict:
        result = super().tags(field)
        messages = [v.message for v in field.validators if (hasattr(v, 'message') and v.message)]
        if messages:
            result['data-parsley-error-message'] = '\n'.join(messages)
        return result

    def URLTags(self, validator: validators.URL):
        if self.url_builtin:
            return {'data-parsley-type': 'url'}
        else:
            return {'data-parsley-pattern': URL_REGEX}

    def DataRequiredTags(self, validator: validators.DataRequired):
        return {'data-parsley-required': 'true'}

    def InputRequiredTags(self, validator: validators.InputRequired):
        return {'data-parsley-required': 'true'}

    def EmailTags(self, validator: validators.Email):
        if self.email_builtin:
            return {'data-parsley-type': 'email'}
        else:
            return {'data-parsley-pattern': EMAIL_REGEX}

    def EqualToTags(self, validator: validators.EqualTo):
        return {'data-parsley-equalto': f'#{validator.fieldname}'}

    def IPAddressTags(self, validator: validators.Email):
        if validator.ipv4 and validator.ipv6:
            return {'data-parsley-pattern': IPV46_REGEX}
        elif validator.ipv4:
            return {'data-parsley-pattern': IPV4_REGEX}
        elif validator.ipv6:
            return {'data-parsley-pattern': IPV6_REGEX}

    def LengthTags(self, validator: validators.Length):
        result = {}
        if validator.min != -1:
            result['data-parsley-minlength'] = validator.min
        if validator.max != -1:
            result['data-parsley-maxlength'] = validator.max
        return result

    def MacAddressTags(self, validator: validators.MacAddress):
        return {'data-parsley-pattern': MAC_REGEX}

    def NumberRangeTags(self, validator: validators.NumberRange):
        if validator.min is None:
            return {'data-parsley-max': validator.max}
        if validator.max is None:
            return {'data-parsley-min': validator.min}
        else:
            return {'data-parsley-range': f'[{validator.min},{validator.max}]'}

    def RegexpTags(self, validator: validators.Regexp):
        return {'data-parsley-pattern': validator.regex.pattern}

    def UUIDTags(self, validator: validators.Regexp):
        return {'data-parsley-pattern': UUID_REGEX}

    def AnyOfTags(self, validator: validators.AnyOf):
        return {'data-parsley-pattern': any_of_regex(validator.values)}

    def NoneOfTags(self, validator: validators.AnyOf):
        return {'data-parsley-pattern': none_of_regex(validator.values)}

    def OptionalTags(self, validator: validators.Optional):
        return {'optional': ''}
