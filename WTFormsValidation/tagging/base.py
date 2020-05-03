"""Base class for tag-based transformers"""

from typing import Dict

from wtforms import Form
from wtforms.fields import Field


class TaggerBase:
    def tags(self, field: Field):
        """Expected to be overloaded by a function that takes a WTForms field,
        and returns a dict render_kw is to be updated with
        """
        raise NotImplementedError

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
