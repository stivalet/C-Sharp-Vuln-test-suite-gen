from jinja2 import Template, DebugUndefined


class ComplexitiesGenerator:

    def __init__(self, complexities_array, template_code, input_type, output_type):
        self.complexities_array = complexities_array
        self.template_code = template_code
        self.input_type = input_type
        self.output_type = output_type
        self.id_class = 0
        self.id_function = 0
        self.uid = 0

        self.complexities = []
        self.complexities.append({'type': None, 'code': "{{filtering_content}}", 'local_var': {}})

        self._executed = True

        self.id_var_in = len(complexities_array)*2
        self.id_var_out = self.id_var_in+1

        self._in_ext_name = None
        self._in_int_name = "tainted_"+str(self.id_var_in)
        self._out_ext_name = None
        self._out_int_name = "tainted_"+str(self.id_var_out)

        self.add_value_dict(self.input_type, self._in_int_name)
        self.add_value_dict(self.output_type, self._out_int_name)

    @property
    def in_ext_name(self):
        return self._in_ext_name

    @property
    def in_int_name(self):
        return self._in_int_name

    @property
    def out_ext_name(self):
        return self._out_ext_name

    @property
    def out_int_name(self):
        return self._out_int_name

    @property
    def executed(self):
        return self._executed

    def get_template(self):
        return self.template_code

    def compose(self):
        for c in reversed(self.complexities_array):
            self._executed = self._executed and c.is_executed()
            # chack if complexities is in 2 parts (code and body)
            if c.indirection:
                t = Template(c.body, undefined=DebugUndefined)
            else:
                t = Template(c.code, undefined=DebugUndefined)
            # generate uid if it's needed
            if c.need_id:
                self.uid += 1

            # if function/class generate a name
            call_name = None
            if c.type == "function":
                self.uid += 1
                call_name = "function_"+str(self.uid)
            elif c.type == "class":
                self.uid += 1
                call_name = "Class_"+str(self.uid)

            # create in/out vars
            in_var, out_var = self.get_in_out_var(c)

            # render on code
            self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name, in_var_type=self.input_type, out_var_type=self.output_type)

            if c.indirection:
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
                # ###################################
                # start a nex stack of complexities #
                #####################################
                self.complexities.insert(0, {'type': None, 'code': c.code, 'local_var': {}})
                t = Template(c.code, undefined=DebugUndefined)
                self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name)
        self.fill_template()


    def fill_template(self):
        self._in_ext_name = "tainted_" + str(self.id_var_in)
        self._out_ext_name = "tainted_" + str(self.id_var_out)
        self.add_value_dict(self.input_type, self._in_ext_name)
        self.add_value_dict(self.output_type, self._out_ext_name)

        # LOCAL VARS
        local_var_code = self.generate_local_var_code(self.complexities[0]['local_var'])

        t = Template(self.template_code, undefined=DebugUndefined)
        self.template_code = t.render(filtering_content=self.complexities[0]['code'], local_var=local_var_code)
        for c in self.complexities[1:]:
            if c['type'] == "class":
                self.template_code = Template(self.template_code, undefined=DebugUndefined).render(classes=c['code']+"\n{{classes}}")
            elif c['type'] == "function":
                self.template_code = Template(self.template_code, undefined=DebugUndefined).render(static_methods=c['code']+"\n{{static_methods}}")

    def generate_local_var_code(self, local_var):
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
        dico = self.complexities[0]['local_var']
        if key not in dico:
            dico[key] = set()
        dico[key].add(value)


    def get_in_out_var(self, c):
        in_var = None
        out_var = None
        if c.in_out_var == "in":
            self.id_var_in -= 1
            in_var = "tainted_"+str(self.id_var_in)
            out_var = "tainted_"+str(self.id_var_in+1)
            self.add_value_dict(self.input_type, in_var)
            self.add_value_dict(self.input_type, out_var)
        elif c.in_out_var == "out":
            in_var = "tainted_"+str(self.id_var_out)
            self.id_var_out += 1
            out_var = "tainted_"+str(self.id_var_out)
            self.add_value_dict(self.output_type, in_var)
            self.add_value_dict(self.output_type, out_var)
        elif c.in_out_var == "traversal":
            in_var = "tainted_"+str(self.id_var_in)
            self.id_var_in -= 1
            out_var = "tainted_"+str(self.id_var_out)
            self.id_var_out += 1
            self.add_value_dict(self.input_type, in_var)
            self.add_value_dict(self.output_type, out_var)
        return in_var, out_var
