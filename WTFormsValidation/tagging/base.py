"""Base class for tag-based transformers"""

from typing import Dict

from wtforms import Form, validators
from wtforms.fields import Field


class TaggerBase:
    def validator_to_dict(self, validator) -> Dict:  # type: ignore
        """Take a validator, and return it in a tag form
        Classes derived from TaggerBase are expected to provide _Tags functions,
        that take the validator as their sole argument.
        e.g. wtforms.validators.Email -> def EmailTags(self, validator: wtforms.validators.Email)
        """
        validator_funcname = f'{type(validator).__name__}Tags'

        if hasattr(validator, 'validate_hostname'):
            # URL validator is really just a regex in disguise
            validator_funcname = 'URLTags'

        if hasattr(self, validator_funcname):
            return getattr(self, validator_funcname)(validator)
        return dict()

    def tags(self, field: Field) -> Dict:
        result = dict()
        for validator in field.validators:
            result.update(self.validator_to_dict(validator))

        return result

    def extend(self, form: Form):
        """Extend the form with checker tags"""
        for field in form:
            tags: Dict = self.tags(field)
            if tags:
                if field.render_kw is None:
                    field.render_kw = tags
                else:
                    field.render_kw.update(tags)
        return form
