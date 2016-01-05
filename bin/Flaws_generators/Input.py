from .InitializeSample import InitialSample


class InputSample(InitialSample):  # Initialize the type of input and the code parameters of the class
    # compatible with new structure
    def __init__(self, initialSample):  # XML tree in parameter
        InitialSample.__init__(self, initialSample)
        self.inputType = initialSample.find("inputType").text
        self.code = initialSample.find("code").text
        self.imports = [imp.text for imp in initialSample.find("imports").findall("import")]

    def __str__(self):
        return "*** Input ***\n{}\n\tinput type : {}\n\timport : {}\n\tcode : {}\n\n".format(super(InputSample, self).__str__(), self.inputType, self.imports, self.code)

    def get_code(self):
        return self.codes

    def get_input_type(self):
        return self.inputType

    def get_imports(self):
        return self.imports
