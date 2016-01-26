

class ConditionSample(object):

    def __init__(self, xml_cond):
        self._id = xml_cond.get("id")
        self._code = xml_cond.find("code").text
        value = xml_cond.find("value").text.lower()
        if value == "true":
            self._value = True
        elif value == "false":
            self._value = False

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value
