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

        dico = self.complexities[0]['local_var']
        if self.input_type not in dico:
            dico[self.input_type] = set()
        if self.output_type not in dico:
            dico[self.output_type] = set()
        dico[self.input_type].add(self._in_int_name)
        dico[self.output_type].add(self._out_int_name)

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
            if c.indirection:
                t = Template(c.body, undefined=DebugUndefined)
            else:
                t = Template(c.code, undefined=DebugUndefined)
            if c.need_id:
                self.uid += 1

            dico = self.complexities[0]['local_var']
            if self.input_type not in dico:
                dico[self.input_type] = set()
            if self.output_type not in dico:
                dico[self.output_type] = set()
            call_name = None
            if c.type == "function":
                self.uid += 1
                call_name = "function_"+str(self.uid)
            elif c.type == "class":
                self.uid += 1
                call_name = "Class_"+str(self.uid)
            in_var = None
            out_var = None
            if c.in_out_var == "in":
                self.id_var_in -= 1
                in_var = "tainted_"+str(self.id_var_in)
                out_var = "tainted_"+str(self.id_var_in+1)
                dico[self.input_type].add(in_var)
                dico[self.input_type].add(out_var)
            elif c.in_out_var == "out":
                in_var = "tainted_"+str(self.id_var_out)
                self.id_var_out += 1
                out_var = "tainted_"+str(self.id_var_out)
                dico[self.input_type].add(in_var)
                dico[self.output_type].add(out_var)
            elif c.in_out_var == "traversal":
                in_var = "tainted_"+str(self.id_var_in)
                self.id_var_in -= 1
                out_var = "tainted_"+str(self.id_var_out)
                self.id_var_out += 1
                dico[self.input_type].add(in_var)
                dico[self.output_type].add(out_var)


            self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name, in_var_type=self.input_type, out_var_type=self.output_type)

            if c.indirection:
                local_var = self.complexities[0]['local_var']
                # LOCAL VARS
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

                self.complexities[0]['code'] = Template(self.complexities[0]['code'], undefined=DebugUndefined).render(local_var=local_var_code)

                self.id_var_in -= 1
                in_var = "tainted_"+str(self.id_var_in)
                self.id_var_out += 1
                out_var = "tainted_"+str(self.id_var_out)
                dico[self.input_type].add(in_var)
                dico[self.output_type].add(out_var)
                self.complexities[0]['type'] = c.type
                tmp = {'type': None, 'code': c.code, 'local_var': {}}
                self.complexities.insert(0, tmp)
                t = Template(c.code, undefined=DebugUndefined)
                self.complexities[0]['code'] = t.render(placeholder=self.complexities[0]['code'], id=self.uid, in_var_name=in_var, out_var_name=out_var, call_name=call_name)
        self.fill_template()

        # self.complexities[-1]['code'] = Template(self.complexities[-1]['code'], undefined=DebugUndefined).render(end_placeholder="{{input_content}}")

    def fill_template(self):
        self._in_ext_name = "tainted_" + str(self.id_var_in)
        self._out_ext_name = "tainted_" + str(self.id_var_out)
        dico = self.complexities[0]['local_var']
        if self.input_type not in dico:
            dico[self.input_type] = set()
        if self.output_type not in dico:
            dico[self.output_type] = set()
        dico[self.input_type].add(self._in_ext_name)
        dico[self.output_type].add(self._out_ext_name)
        # LOCAL VARS
        local_var = self.complexities[0]['local_var']
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
        t = Template(self.template_code, undefined=DebugUndefined)
        self.template_code = t.render(filtering_content=self.complexities[0]['code'], local_var=local_var_code)
        for c in self.complexities[1:]:
            if c['type'] == "class":
                self.template_code = Template(self.template_code, undefined=DebugUndefined).render(classes=c['code']+"\n{{cclasses}}")
            elif c['type'] == "function":
                self.template_code = Template(self.template_code, undefined=DebugUndefined).render(static_methods=c['code']+"\n{{static_methods}}")
