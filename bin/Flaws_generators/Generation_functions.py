import xml.etree.ElementTree as ET
import re
import copy

from .Input import InputSample
from .Filtering import FilteringSample
from .Sink import SinkSample

from Classes.FileManager import *
from Classes.File import *
import global_variables as g


def cwe_test(first_intersection):
    if len(g.cwe_list) == 0:
        return first_intersection
    first_intersection_cwe = []
    for cwe in first_intersection:
        first_intersection_cwe.append(re.findall("_([0-9]+)_", cwe)[0])
    if set(g.cwe_list).intersection(first_intersection_cwe):
        return True
    return False


def f_construction(generator, root, params, i):
    global decorators
    tree_construction = ET.parse(FileManager.getXML("sink")).getroot()
    for c in tree_construction:
        params[i] = SinkSample(c)
        print(params[i])
        if cwe_test(set(generator.getType()).intersection(params[i].flaws)):
            generation(generator, root, params, i + 1)
    decorators[i] = []


def f_sanitize(generator, root, params, i):
    global decorators
    tree_sanitize = ET.parse(FileManager.getXML("filtering")).getroot()
    for s in tree_sanitize:
        params[i] = FilteringSample(s)
        print(params[i])
        if cwe_test(set(generator.getType()).intersection(params[i].flaws)):
            generation(generator, root, params, i + 1)
    decorators[i] = []


def f_input(generator, root, params, i):
    global decorators
    tree_input = ET.parse(FileManager.getXML("input")).getroot()
    for Input in tree_input:
        params[i] = InputSample(Input)
        print(params[i])
        generation(generator, root, params, i + 1)
    decorators[i] = []


# TODO
def f_decorator(params, decorators, i):
    pass

options = {
    "construction": f_construction,
    "sanitize": f_sanitize,
    "input": f_input,
}


def initialization(generator, root):
    params = [None] * len(root)
    global decorators
    decorators = [[] for x in range(0, len(root))]
    global postOp
    postOp = []
    generation(generator, root, params)
    return generator.safe_Sample, generator.unsafe_Sample

def is_safe_selection(input, filtering, sink):
    return input.is_safe() or filtering.is_safe(sink.get_cwe()) or sink.is_safe()


def generation(generator, root, params, i=0):
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
