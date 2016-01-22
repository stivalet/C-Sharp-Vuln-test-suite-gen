import os
import time


class Manifest:

    def __init__(self, dir_name, date):
        self.dir_name = dir_name
        self.date = date
        self.manifest = {}

    def createManifests(self, flaw_groups):
        for flaw_group in flaw_groups:
            path = self.dir_name + "/" + flaw_group + "/"
            if not os.path.exists(path):
                os.makedirs(path)
            self.manifest[flaw_group] = open(path + "manifest.xml", "w+")
        for group in self.manifest:
            self.manifest[group].write("<container>\n")

    def addTestCase(self, input_sample, flaw_group, flaw, flaw_line, file_path):
        reformated_date = time.strftime("%d/%m/%y", time.strptime(self.date, "%m-%d-%Y_%Hh%Mm%S"))
        meta_data = ("\t<testcase> \n" +
                     "\t\t<meta-data> \n" +
                     "\t\t\t<author>Bertrand STIVALET, Aurelien DELAITRE</author> \n" +
                     "\t\t\t<date>" + reformated_date + "</date> \n" +
                     "\t\t\t<input>" + input_sample.split(":")[1][1:] + "</input>\n" +  # truncate "input : "
                     "\t\t</meta-data> \n \n")

        self.manifest[flaw_group].write(meta_data)

        if (flaw_line == 0):
            file_block = "\t\t<file path=\"" + file_path + "\" language=\"Csharp\"/> \n\n"
        else:
            file_block = "\t\t<file path=\"" + file_path + "\" language=\"Csharp\"> \n"
            file_block += "\t\t\t<flaw line=\"" + str(flaw_line) + "\" name =\"" + flaw + "\"/> \n"
            file_block += "\t\t</file> \n\n"

        self.manifest[flaw_group].write(file_block)
        self.manifest[flaw_group].write("\t</testcase> \n\n\n")

    def closeManifests(self):
        for man in self.manifest:
            self.manifest[man].write("</container>")
            self.manifest[man].close()
