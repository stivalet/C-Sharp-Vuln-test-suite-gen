import xml.etree.ElementTree as ET
import re
import copy

from .Input import InputSample
from .Filtering import FilteringSample
from .Sink import SinkSample

from Classes.FileManager import FileManager
from Classes.File import File


# TODO remove this ?
def cwe_test(first_intersection):
    if len(g.cwe_list) == 0:
        return first_intersection
    first_intersection_cwe = []
    for cwe in first_intersection:
        first_intersection_cwe.append(re.findall("_([0-9]+)_", cwe)[0])
    if set(g.cwe_list).intersection(first_intersection_cwe):
        return True
    return False


def is_safe_selection(input, filtering, sink):
    return input.is_safe() or filtering.is_safe(sink.get_flaw_type()) or sink.is_safe()


def initialization(params):
    tree_input = ET.parse(FileManager.getXML("input")).getroot()
    tab_input = [InputSample(inp) for inp in tree_input]

    tree_filtering = ET.parse(FileManager.getXML("filtering")).getroot()
    tab_filtering = [FilteringSample(filtering) for filtering in tree_filtering]

    tree_sink = ET.parse(FileManager.getXML("sink")).getroot()
    tab_sink = [SinkSample(sink) for sink in tree_sink]

    generation(params, tab_input, tab_filtering, tab_sink)


def generation(params, inputs, filterings, sinks):
    # TODO check params : ex CWE_XXX, URF, ...

    for sink in sinks:
        flaw_type = sink.get_flaw_type()
        # TODO check if sink need filtering or input

        for filtering in filterings:
            # check if sink and filtering are compatibles
            if sink.compatible_with(filtering):
                # TODO check if filtering need input

                for inp in inputs:
                    # check if types are equals
                    if filtering.get_input_type() == inp.get_output_type():
                        decorator(params, inp, filtering, sink)


# TODO complexities
def decorator(params, inp, filtering, sink):
    print("#########################")
    print("safe : "+str(is_safe_selection(inp, filtering, sink)))
    print(inp)
    print(filtering)
    print(sink)


# TODO remove this
def generation_old(generator, root, params, i=0):
    global postOp
    global decorators
    global function_cpt
    function_cpt = 1
    global class_cpt
    class_cpt = 1
    global file_cpt
    file_cpt = 1
    if i < len(root):
        pos = root[i]
        while len(pos) > 0:
            decorators[i].append(pos)
            pos = pos[0]
        options[pos.tag](generator, root, params, i)
    else:
        tmp = copy.deepcopy(params)
        for i in range(0, len(root)):
            f_decorator(tmp, decorators, i)
        file = generator.generate(tmp)
        if file is None:
            postOp = []
        while len(postOp) > 0:
            pop = postOp.pop()
            if pop is None:
                break
            if isinstance(pop, File):
                pop.setPath(file.getPath())
                FileManager.createFile(pop)
                file_cpt -= 1
