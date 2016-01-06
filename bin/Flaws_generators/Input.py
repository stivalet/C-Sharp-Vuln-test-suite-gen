from .InitializeSample import InitialSample


class InputSample(InitialSample):  # Initialize the type of input and the code parameters of the class
    # compatible with new structure
    def __init__(self, initialSample):  # XML tree in parameter
        InitialSample.__init__(self, initialSample)
        self.input_type = initialSample.find("input_type").text.lower()
        self.output_type = initialSample.find("output_type").text.lower()
        self.code = initialSample.find("code").text


    def __str__(self):
        return "*** Input ***\n{}\n\tinput type : {}\n\toutput type : {}\n\tcode : {}\n\
            \n".format(super(InputSample, self).__str__(),
                       self.input_type,
                       self.output_type,
                       self.code)

    def get_code(self):
        return self.code

    def get_input_type(self):
        return self.input_type

    def get_output_type(self):
            return self.output_type
