"""
ComplexitiesGenerator Class (TODO DOC)
"""

from jinja2 import Template, DebugUndefined
import c_sharp_vuln_test_suite_gen.generator


class ComplexitiesGenerator(object):

    def __init__(self, complexities_array, template_code, input_type, output_type, filtering):
        self.complexities_array = complexities_array
        """ list of selected complexities """
        self.template_code = template_code
        """ template code """
        self.input_type = input_type
        """ input type """
        self.output_type = output_type
        """ output type """
        self.filtering = filtering
        """ current filtering """
        self.uid = 0
        """ uid for variables/functions/classes name """

        self.complexities = []
        """ dict with complexities, type (function/class) and local var for composition """
        self.complexities.append({'type': None, 'code': "{{filtering_content}}", 'local_var': {}, 'name': ""})

        self._executed = True
        """ True if the final flaceholder will be executed """

        self.id_var_in = len(complexities_array)*2
        """ id for interne variables to join complexities """
        self.id_var_out = self.id_var_in+1
        """ id for interne variables to join complexities """

        self._in_ext_name = None
        """ name of external intput variable (for input) """
        self._in_int_name = "tainted_"+str(self.id_var_in)
        """ name of internal intput variable (for filtering) """
        self._out_ext_name = None
        """ name of external output variable (for sink) """
        self._out_int_name = "tainted_"+str(self.id_var_out)
        """ name of internal output variable (for filtering) """

        self.add_value_dict(self.input_type, self._in_int_name)
        self.add_value_dict(self.output_type, self._out_int_name)

    @property
    def in_ext_name(self):
        """ Get input extrenal variable name """
        return self._in_ext_name

    @property
    def in_int_name(self):
        """ Get input internal variable name """
        return self._in_int_name

    @property
    def out_ext_name(self):
        """ Get output external variable name """
        return self._out_ext_name

    @property
    def out_int_name(self):
        """ Get output internal variable name """
        return self._out_int_name

    @property
    def executed(self):
        """ Get if placeholder code is executed """
        return self._executed

    def get_template(self):
        """ Get modifies template """
        return self.template_code

    def compose(self):
        """
        This method compose all complexities.
        """
        for c in reversed(self.complexities_array):
            self._executed = self._executed and c.is_executed()
            # check if complexities is in 2 parts (code and body)
            if c.indirection and c.in_out_var == "traversal":
                t = Template(c.body, undefined=DebugUndefined)
            else:
                t = Template(c.code, undefined=DebugUndefined)
            # generate uid if it's needed

            # if function/class generate a name
            call_name = None
            if c.type == "function":
                self.uid = c_sharp_vuln_test_suite_gen.generator.Generator.getUID()
                call_name = "function_"+str(self.uid)
            elif c.type == "class":
                self.uid = c_sharp_vuln_test_suite_gen.generator.Generator.getUID()
                call_name = "Class_"+str(self.uid)

            # create in/out vars
            in_var, out_var = self.get_in_out_var(c)

            # render on code
            self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name, in_var_type=self.input_type, out_var_type=self.output_type)

            # trasversol for class/function where the placeholder is in the body of function/class
            if c.indirection and c.in_out_var == "traversal":
                # LOCAL VARS
                local_var_code = self.generate_local_var_code(self.complexities[0]['local_var'])
                # put local var on body
                self.complexities[0]['code'] = Template(self.complexities[0]['code'], undefined=DebugUndefined).render(local_var=local_var_code)
                # add in_var
                self.id_var_in -= 1
                in_var = "tainted_"+str(self.id_var_in)
                self.add_value_dict(self.input_type, in_var)
                # add out_var
                self.id_var_out += 1
                out_var = "tainted_"+str(self.id_var_out)
                self.add_value_dict(self.output_type, out_var)
                # change type of current complexities
                self.complexities[0]['type'] = c.type
                if c.type == "class":
                    self.complexities[0]['type'] = "class_trasversal"
                elif c.type == "function":
                    self.complexities[0]['type'] = "function_trasversal"
                self.complexities[0]['name'] = call_name
                # ###################################
                # start a nex stack of complexities #
                #####################################
                # insert new dict for the next complexity
                self.complexities.insert(0, {'type': None, 'code': c.code, 'local_var': {}, 'name': ""})
                t = Template(c.code, undefined=DebugUndefined)
                self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name)
            # in case if the placeholder is before or after the call to class/function
            elif c.indirection and (c.in_out_var == "in" or c.in_out_var == "out"):
                if c.type == "class":
                    body = Template(c.body, undefined=DebugUndefined).render(id=self.uid, in_var_type=self.input_type, out_var_type=self.output_type, call_name=call_name)
                    self.complexities.insert(1, {'type': "class", 'code': body, 'local_var': {}, 'name': call_name})
                elif c.type == "function":
                    body = Template(c.body).render(id=self.uid, in_var_type=self.input_type, out_var_type=self.output_type, call_name=call_name)
                    self.complexities.insert(1, {'type': "function", 'code': body, 'local_var': {}, 'name': call_name})

        return self.fill_template()

    def fill_template(self):
        """
        This method fill template with previous compose complexities with local var and instructions
        """
        # name of external variable to join with input and sink
        self._in_ext_name = "tainted_" + str(self.id_var_in)
        self._out_ext_name = "tainted_" + str(self.id_var_out)
        # add to list with local var
        self.add_value_dict(self.input_type, self._in_ext_name)
        self.add_value_dict(self.output_type, self._out_ext_name)

        functions_code = ""
        classes_code = []
        # compose complexity i inti i-1
        for c in reversed(self.complexities[1:]):
            if c['type'] == "class_trasversal":
                # add a new class code when we have a trasversal class
                imports_content = "\n".join(["using {};".format(import_content) for import_content in set(self.filtering.imports)])
                classes_code.append({'code': Template(c['code'], undefined=DebugUndefined).render(static_methods=functions_code, imports=imports_content), 'name': c['name']})
                functions_code = ""
            elif c['type'] == "class":
                classes_code.append({'code': c['code'], 'name': c['name']})
            elif c['type'] == "function_trasversal":
                functions_code += Template(c['code'], undefined=DebugUndefined).render(static_methods=functions_code)
            elif c['type'] == "function":
                functions_code += c['code'] + "\n\n"

        # generate local vars
        local_var_code = self.generate_local_var_code(self.complexities[0]['local_var'])
        t = Template(self.template_code, undefined=DebugUndefined)
        # fill template with local vars, complexities and static methods
        self.template_code = t.render(filtering_content=self.complexities[0]['code'], local_var=local_var_code, static_methods=functions_code)
        # return all classes not in the main file
        return classes_code

    def generate_local_var_code(self, local_var):
        """ Generate local var with type, name and initialisation """
        # TODO hardcoded string/int/null ...
        local_var_code = ""
        for t in local_var:
            init = ""
            if t == "string":
                local_var_code += "string "
                init = "null"
            elif t == "int":
                local_var_code += "int "
                init = "0"
            else:
                local_var_code += "//ERROR type '" + t + "' "
            for i, n in enumerate(list(local_var[t])):
                local_var_code += n + " = "+init
                if i < len(local_var[t])-1:
                    local_var_code += ", "
                else:
                    local_var_code += ";\n"
        return local_var_code

    def add_value_dict(self, key, value):
        """ Add a variable name into a dict. This dict is compile after for local var """
        dico = self.complexities[0]['local_var']
        if key not in dico:
            dico[key] = set()
        dico[key].add(value)

    def get_in_out_var(self, c):
        """ Generated name for variable in different cases (in/trasversal/out)"""
        in_var = None
        out_var = None
        if c.in_out_var == "in":
            # just change input var name
            self.id_var_in -= 1
            in_var = "tainted_"+str(self.id_var_in)
            out_var = "tainted_"+str(self.id_var_in+1)
            self.add_value_dict(self.input_type, in_var)
            self.add_value_dict(self.input_type, out_var)
        elif c.in_out_var == "out":
            # just change output var name
            in_var = "tainted_"+str(self.id_var_out)
            self.id_var_out += 1
            out_var = "tainted_"+str(self.id_var_out)
            self.add_value_dict(self.output_type, in_var)
            self.add_value_dict(self.output_type, out_var)
        elif c.in_out_var == "traversal":
            # change input/output var name
            in_var = "tainted_"+str(self.id_var_in)
            self.id_var_in -= 1
            out_var = "tainted_"+str(self.id_var_out)
            self.id_var_out += 1
            self.add_value_dict(self.input_type, in_var)
            self.add_value_dict(self.output_type, out_var)
        return in_var, out_var
