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


class InitialSample:  # Initialize path and comment
    # compatible with new structure
    def __init__(self, initialSample):  # XML tree in parameter
        self.path = []
        tree_path = initialSample.find("path").findall("dir")
        for dir in tree_path:
            self.path.append(dir.text)

        self.comment = initialSample.find("comment").text

        self.imports = []
        if initialSample.find("imports"):
            self.imports = [imp.text for imp in initialSample.find("imports").findall("import")]

    def __str__(self):
        return "\tpath : {}\n\t\
                comment : {}\n\t\
                imports : {}\
                ".format(self.path,
                         self.comment,
                         self.imports)

    def get_path(self):
        return self.path

    def get_imports(self):
        return self.imports

    def addSafetyAttributes(self, initialSample):
        # Classify XSS injection/sanitization by rule of OWASP
        safeties = initialSample.find("safeties").findall("safety")
        for safety in safeties:
            if "XSS" in safety.get("flawType"):
                # Rule of sanitizing needed
                self.safeties[safety.get("flawType")]["rule"] = 0
                if safety.get("rule") is not None:
                    self.safeties[safety.get("flawType")]["rule"] = int(safety.get("rule"))

                # Escaping simple quoted is enough ?
                self.safeties[safety.get("flawType")]["simpleQuote"] = 0
                if safety.get("simpleQuote") is not None:
                    self.safeties[safety.get("flawType")]["simpleQuote"] = int(safety.get("simpleQuote"))

                # Escaping double quoted is enough ?
                self.safeties[safety.get("flawType")]["doubleQuote"] = 0
                if safety.get("doubleQuote") is not None:
                    self.safeties[safety.get("flawType")]["doubleQuote"] = int(safety.get("doubleQuote"))

                # Unsafe function & co
                self.safeties[safety.get("flawType")]["unsafe"] = 0
                if safety.get("unsafe") is not None:
                    self.safeties[safety.get("flawType")]["unsafe"] = int(safety.get("unsafe"))

                # Escape of type " -> \" needed ? (TODO : improve that)
                self.safeties[safety.get("flawType")]["escape"] = 0
                if safety.get("escape") is not None:
                    self.safeties[safety.get("flawType")]["escape"] = int(safety.get("escape"))

                # Escape of </script> needed ?
                self.safeties[safety.get("flawType")]["scriptBlock"] = 0
                if safety.get("scriptBlock") is not None:
                    self.safeties[safety.get("flawType")]["scriptBlock"] = int(safety.get("scriptBlock"))

                # Escape of </style> needed ?
                self.safeties[safety.get("flawType")]["styleBlock"] = 0
                if safety.get("styleBlock") is not None:
                    self.safeties[safety.get("flawType")]["styleBlock"] = int(safety.get("styleBlock"))

                # Prevent data from starting with "javascript" needed ?
                self.safeties[safety.get("flawType")]["URL_CSS_context"] = 0
                if safety.get("URL_CSS_context") is not None:
                    self.safeties[safety.get("flawType")]["URL_CSS_context"] = int(safety.get("URL_CSS_context"))

                # Prevent data from starting with "expression" needed ?
                self.safeties[safety.get("flawType")]["property_CSS_context"] = 0
                if safety.get("property_CSS_context") is not None:
                    self.safeties[safety.get("flawType")]["property_CSS_context"] = int(safety.get("property_CSS_context"))
