from c_sharp_vuln_test_suite_gen.sample import Sample


class ExecQuerySample(Sample):

    # new version for new XML
    def __init__(self, sample):  # XML tree in parameter
        Sample.__init__(self, sample)
        self._type = sample.get("type").lower()
        self._code = sample.find("code").text
        self._safe = sample.get("safe") == "1"

    def __str__(self):
        return "*** ExecQuery ***\n\ttype : {}\n\tcode : {}\n\
            \n".format(self.type,
                       self.code)

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code

    @property
    def safe(self):
        return self._safe
