

class FileTemplate:

    def __init__(self, file_template):
        self._file_extension = file_template.find("file_extension").text
        self._code = file_template.find("code").text
        self._comment = {}
        self._comment['open'] = file_template.find("comment").find("open").text
        self._comment['close'] = file_template.find("comment").find("close").text
        self._comment['inline'] = file_template.find("comment").find("inline").text

    @property
    def code(self):
        return self._code

    @property
    def file_extension(self):
        return self._file_extension

    @property
    def comment(self):
        return self._comment