import shutil
from Classes.Manifest import Manifest
from .Input import InputSample
from .Filtering import FilteringSample
from .Sink import SinkSample
from .ExecQuery import ExecQuerySample
from Classes.FileManager import FileManager
from Classes.File import File
import xml.etree.ElementTree as ET


class Generator():

    def __init__(self, date):
        self.date = date
        # TODO readd this for manifest generation
        # self.manifest = Manifest(date, flaw)
        self.safe_Sample = 0
        self.unsafe_Sample = 0
        # parse XML files
        tree_input = ET.parse(FileManager.getXML("input")).getroot()
        self.tab_input = [InputSample(inp) for inp in tree_input]
        tree_filtering = ET.parse(FileManager.getXML("filtering")).getroot()
        self.tab_filtering = [FilteringSample(filtering) for filtering in tree_filtering]
        tree_sink = ET.parse(FileManager.getXML("sink")).getroot()
        self.tab_sink = [SinkSample(sink) for sink in tree_sink]
        tree_exec_query = ET.parse(FileManager.getXML("exec_queries")).getroot()
        self.tab_exec_queries = [ExecQuerySample(exec_query) for exec_query in tree_exec_query]
        # set current samples
        self.current_input = None
        self.current_filtering = None
        self.current_sink = None
        self.current_exec_queries = None
        self.current_code = None

    def is_safe_selection(self):
        return self.current_input.is_safe() or self.current_filtering.is_safe(self.current_sink.get_flaw_type()) or self.current_sink.is_safe()

    def generate(self):
        # TODO check params : ex CWE_XXX, URF, ...
        self.select_sink()

    # fist step : browse sink
    def select_sink(self):
        for sink in self.tab_sink:
            self.current_sink = sink
            # TODO check if sink need filtering or input
            self.select_filtering()

    # second step : browse filtering
    def select_filtering(self):
        # select filtering
        for filtering in self.tab_filtering:
            self.current_filtering = filtering
            # check if sink and filtering are compatibles
            if self.current_sink.compatible_with_filtering(filtering):
                # TODO check if filtering need input
                self.select_input()

    # third step : browse input
    def select_input(self):
        # select input
        for inp in self.tab_input:
            if self.current_filtering.get_input_type() == inp.get_output_type():
                self.current_input = inp
                self.select_complexities()

    # fourth step : browse complexities
    def select_complexities(self):
        self.select_exec_queries()

    # fifth step : browse exec_queries
    def select_exec_queries(self):
        if self.current_sink.need_exec():
            # select exec_queries
            for exec_query in self.tab_exec_queries:
                if self.current_sink.compatible_with_exec_queries(exec_query):
                    self.current_exec_queries = exec_query
                    self.compose()
        else:
            self.current_exec_queries = None
            self.compose()

    # seventh step : compose previous code chunks
    def compose(self):
        # TODO replace placeholder on complexities by input/filtering/sink/exec_queries
        # temporary code
        self.current_code = ""
        self.current_code += str(self.current_input.get_code())
        self.current_code += str(self.current_filtering.get_code())
        self.current_code += str(self.current_sink.get_code())
        if self.current_exec_queries:
            self.current_code += str(self.current_exec_queries.get_code())
        self.write_files()

    # eighth step : write on disk and update manifest
    def write_files(self):
        # TODO write on file
        print("#########################################")
        print("safe : "+str(self.is_safe_selection()))
        print(self.current_code)
        print("#########################################")
        # TODO update Manifest

    def getType(self):
        pass

    def generateFileName(self, params, name):
        for param in params:
            name += "__"
            for dir in param.path:
                    name += dir+"-"
            name = name[:-1]
        return name

    def onDestroy(self, flaw):
        self.manifest.close()
        if self.safe_Sample+self.unsafe_Sample > 0:
            print(flaw + " generation report:")
            print(str(self.safe_Sample) + " safe samples")
            print(str(self.unsafe_Sample) + " unsafe samples")
            print(str(self.unsafe_Sample + self.safe_Sample) + " total\n")
        else:
            shutil.rmtree("../CsharpTestSuite_"+self.date+"/"+flaw)

    @staticmethod
    def findFlaw(fileName):
        sample = open(fileName, 'r')
        i = 0
        for line in sample.readlines():
            i += 1
            if line[:6] == "//flaw":
                break
        return i + 1