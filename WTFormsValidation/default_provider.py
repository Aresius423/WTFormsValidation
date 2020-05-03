from WTFormsValidation.tagging import YairEOtagger


class DefaultProvider:
    def __init__(self):
        """Provide lazy-loading instances of the transformers"""
        self.instance_yaireo = None
        self.instance_parsley = None
        self.instance_bounce = None
        self.instance_justvalidate = None
        self.instance_pristine = None
        self.instance_jqvalidate = None

    def yaireo(self) -> YairEOtagger:
        if self.instance_yaireo is None:
            self.instance_yaireo = YairEOtagger()
        return self.instance_yaireo


default_provider = DefaultProvider()
