from .InitializeSample import InitialSample


class SinkSample(InitialSample):  # Load parameters and code beginning and end
    # new version for new XML
    def __init__(self, initialSample):  # Add parameters showing the beginning and the end of the sample
        InitialSample.__init__(self, initialSample)

        self.input_type = initialSample.find("input_type").text.lower()
        self.exec_type = initialSample.find("exec_type").text.lower()
        self.flaw_type = initialSample.find("flaw_type").text
        self.safe = (initialSample.find("safe").text == "1")
        self.code = [code.text for code in initialSample.find("codes").findall("code")]

    def __str__(self):
        return "*** Sink ***\n{}\n\tinput type : {}\n\texec type : {}\n\tflaw type : {}\n\tsafe : {}\n\tcode : {}\n\
            \n".format(super(SinkSample, self).__str__(),
                       self.input_type,
                       self.exec_type,
                       self.flaw_type,
                       self.safe,
                       self.get_code())

    def need_exec(self):
        return self.exec_type != "none"

    def get_exec_type(self):
        return self.exec_type

    def get_input_type(self):
        return self.input_type

    def get_code(self):
        return self.code[0]

    def get_flaw_type(self):
        return self.flaw_type

    def is_safe(self):
        return self.safe

    def compatible_with(self, filteringSample):
        return filteringSample.contain_flaw_type(self.get_flaw_type)
