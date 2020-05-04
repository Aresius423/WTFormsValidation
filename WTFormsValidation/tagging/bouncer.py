"""Class for providing Bouncer.js style tags"""

from typing import Dict, List

from wtforms.fields import Field
from wtforms import validators

from WTFormsValidation.tagging.base import TaggerBase
from WTFormsValidation.regex_utils import EMAIL_REGEX, IPV4_REGEX, IPV6_REGEX, \
        IPV46_REGEX, MAC_REGEX, URL_REGEX, UUID_REGEX, any_of_regex, none_of_regex


class BouncerTagger(TaggerBase):
    """Class for providing Bouncer.js style tags"""
    def __init__(self, email_builtin=False, url_builtin=False):
        """Constructor for the class.

        @param email_builtin: Setting this will use Bouncer.js's e-mail validator, but will set type="email" on the field
        @param url_builtin: Setting this will use Bouncer.js's URL validator, but will set type="email" on the field
        """
        self.email_builtin = email_builtin
        self.url_builtin = url_builtin

    def tags(self, field: Field) -> Dict:
        result = super().tags(field)
        messages = [v.message for v in field.validators if (hasattr(v, 'message') and v.message)]
        if messages:
            result['data-bouncer-message'] = '\n'.join(messages)
        return result


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

    def IPAddressTags(self, validator: validators.Email):
        if validator.ipv4 and validator.ipv6:
            return {'pattern': IPV46_REGEX}
        elif validator.ipv4:
            return {'pattern': IPV4_REGEX}
        elif validator.ipv6:
            return {'pattern': IPV6_REGEX}

    def LengthTags(self, validator: validators.Length):
        result = {}
        if validator.min != -1:
            result['minlength'] = validator.min
        if validator.max != -1:
            result['maxlength'] = validator.max
        return result

    def MacAddressTags(self, validator: validators.MacAddress):
        return {'pattern': MAC_REGEX}

    def NumberRangeTags(self, validator: validators.NumberRange):
        result = {}
        if validator.min is not None:
            result['min'] = validator.min
        if validator.max is not None:
            result['max'] = validator.max
        return result

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
