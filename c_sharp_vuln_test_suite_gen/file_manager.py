import os


class FileManager:

    def __init__(self):
        self.path = ".."
        self.content = ""
        self.name = ""

    def createFile(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        createdFile = open(self.path + "/" + self.name, "w")
        createdFile.write(self.content)
        createdFile.close()

    _xml = {
        "input": "input.xml",
        "filtering": "filtering.xml",
        "sink": "sink.xml",
        "exec_queries": "exec_queries.xml",
        "file_template": "file_template.xml",
        "complexities": "complexities.xml",
    }

    @classmethod
    def getXML(cls, xmlfile):
        return "c_sharp_vuln_test_suite_gen/templates/" + cls._xml[xmlfile]

    # Getters and setters
    def setPath(self, path):
        self.path = path

    def addPath(self, path):
        self.path += "/" + path

    def getPath(self):
        return self.path

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addContent(self, content):
        self.content += content