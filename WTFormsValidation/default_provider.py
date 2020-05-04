from WTFormsValidation.tagging import YairEOtagger, ParsleyTagger, BouncerTagger


class DefaultProvider:
    def __init__(self):
        """Provide lazy-loading instances of the transformers"""
        self.instance_yaireo = None
        self.instance_parsley = None
        self.instance_bouncer = None
        self.instance_justvalidate = None
        self.instance_pristine = None
        self.instance_jqvalidate = None

    def yaireo(self) -> YairEOtagger:
        if self.instance_yaireo is None:
            self.instance_yaireo = YairEOtagger()
        return self.instance_yaireo

    def parsley(self) -> ParsleyTagger:
        if self.instance_parsley is None:
            self.instance_parsley = ParsleyTagger()
        return self.instance_parsley

    def bouncer(self) -> BouncerTagger:
        if self.instance_bouncer is None:
            self.instance_bouncer = BouncerTagger()
        return self.instance_bouncer


default_provider = DefaultProvider()
