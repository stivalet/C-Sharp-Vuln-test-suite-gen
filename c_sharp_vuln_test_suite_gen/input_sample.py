from c_sharp_vuln_test_suite_gen.sample import Sample


class InputSample(Sample):  # Initialize the type of input and the code parameters of the class
    # compatible with new structure
    def __init__(self, sample):  # XML tree in parameter
        Sample.__init__(self, sample)
        self._input_type = sample.find("input_type").text.lower()
        self._output_type = sample.find("output_type").text.lower()
        self._code = sample.find("code").text
        self._flaws = {}
        for flaw in sample.find("flaws").findall("flaw"):
            flaw_type = flaw.get("flaw_type")
            self._flaws[flaw_type] = {}
            self._flaws[flaw_type]["safe"] = (flaw.get("safe") == "1")

    def __str__(self):
        return "*** Input ***\n{}\n\tinput type : {}\n\toutput type : {}\n\tflaws : {}\n\tcode : {}\n\
            \n".format(super(InputSample, self).__str__(),
                       self.input_type,
                       self.output_type,
                       self.flaws,
                       self.code)

    def is_safe(self, flaw_type):
        if flaw_type in self.get_flaws_types():
            return self.flaws[flaw_type]["safe"]
        if "default" in self.get_flaws_types():
            return self.flaws["default"]["safe"]
        return None

    @property
    def code(self):
        return self._code

    @property
    def input_type(self):
        return self._input_type

    @property
    def output_type(self):
            return self._output_type

    def compatible_with_filtering_sink(self, filtering, sink):
        if filtering.input_type != "nofilter":
            return self.output_type == filtering.input_type
        else:
            return self.output_type == sink.input_type

    @property
    def flaws(self):
        return self._flaws

    def get_flaws_types(self):
        return self.flaws.keys()