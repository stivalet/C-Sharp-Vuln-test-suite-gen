import os
import sys
import time
import getopt

# Constants
safe = "safe"
unsafe = "unsafe"
needQuote = "needQuote"
quote = "quote"
noQuote = "noQuote"
integer = "int"
safety = "safety"
# block = "block"
# noBlock = "noBlock"
prepared = "prepared"
noPrepared = "noPrepared"
needUrlSafe = "needUrlSafe"
urlSafe = "urlSafe"
needErrorSafe = "needErrorSafe"
errorSafe = "errorSafe"


class Sample:  # Initialize path and comment
    # compatible with new structure
    def __init__(self, sample):  # XML tree in parameter
        self._path = []
        tree_path = sample.find("path").findall("dir")
        for dir in tree_path:
            self.path.append(dir.text)

        self._comment = sample.find("comment").text

        self._imports = []
        if sample.find("imports"):
            self._imports = [imp.text for imp in sample.find("imports").findall("import")]

    def __str__(self):
        return "\tpath : {}\n\tcomment : {}\n\timports : {}\
                ".format(self.path,
                         self.comment,
                         self.imports)

    def generate_file_name(self):
        name = ""
        for directory in self.path:
            name += directory+"-"
        name = name[:-1]
        return name

    @property
    def path(self):
        return self._path

    @property
    def imports(self):
        return self._imports

    @imports.setter
    def imports(self, value):
        self._imports = value

    @property
    def comment(self):
        return self._comment
