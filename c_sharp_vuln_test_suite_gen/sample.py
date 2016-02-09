"""
Sample Class (TODO DOC)
"""


class Sample(object):

    def __init__(self, sample):
        self._path = []
        """ path for identify the sample """
        tree_path = sample.find("path").findall("dir")
        for dir in tree_path:
            self.path.append(dir.text)

        self._comment = sample.find("comment").text
        """ comment for sample """
        self._imports = []
        if sample.find("imports") is not None:
            self._imports = [imp.text for imp in sample.find("imports").findall("import")]

        self._need_id = False
        """ true if sample need id for code chunk """
        if sample.get("need_id") == "1":
            self._need_id = True

        self._safe = False
        self._unsafe = False
        if sample.find("safety") is not None:
            self._safe = sample.find("safety").get("safe") == "1"
            self._unsafe = sample.find("safety").get("unsafe") == "1"

    def __str__(self):
        return "\tpath : {}\n\tcomment : {}\n\timports : {}\
                ".format(self.path,
                         self.comment,
                         self.imports)

    @property
    def safe(self):
        return self._safe

    @property
    def unsafe(self):
        return self._unsafe

    @property
    def need_id(self):
        return self._need_id

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
