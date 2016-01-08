

class ExecQuerySample:

    # new version for new XML
    def __init__(self, sample):  # XML tree in parameter
        self._type = str(sample.get("type"))
        self._imports = []
        if sample.find("imports"):
            self._imports = [imp.text for imp in sample.find("imports").findall("import")]
        self._code = sample.find("code").text

    def __str__(self):
        return "*** ExecQuery ***\n\ttype : {}\n\timorts : {}\n\tcode : {}\n\
            \n".format(self.type,
                       self.imports,
                       self.code)

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code[0]

    @property
    def imports(self):
        return self._imports