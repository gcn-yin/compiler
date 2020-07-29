class CodeBuilder:

    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    def __str__(self):
        return ''.join(str(i) for i in self.code)

    def add_line(self, line):
        self.code.append(" " * self.indent_level + line + '\n')

    def add_section(self):
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section        

    INDENT_STEP = 4

    def indent(self):
        self.indent_level += CodeBuilder.INDENT_STEP

    def dedent(self):
        self.indent_level -= CodeBuilder.INDENT_STEP
        if self.indent_level < 0:
            raise Exception("Error: Indent level has been negative.")

    def get_globals(self):
        if self.indent_level != 0:
            raise Exception("Error: Indent level doesn't equal zero.")
        python_source = str(self)
        global_namespace = dict()
        exec(python_source, global_namespace)
        return global_namespace
