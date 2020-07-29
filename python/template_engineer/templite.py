import re
from codebuilder import CodeBuilder

class TempliteSyntaxError(ValueError):
    pass


class Templite(object):

    def __init__(self, text, *contexts):
        self.text = text
        self.context = self.create_context(contexts)
        self.all_vars = set()
        self.loop_vars = set()
        self.vars_code = None
        self.code = self.codebudiler()
        self.buffered = []
        self.ops_stack = []
        self.flush_output()
        self.compiler()

    def create_context(self, contexts):
        context = dict()
        for context_ele in contexts:
            context.update(context_ele)
        return context

    def codebudiler(self):
        code = CodeBuilder()
        code.add_line("def render_function(context, do_dots):")
        code.indent()
        self.vars_code = code.add_section()
        code.add_line("result = []")
        code.add_line("append_result = result.append")
        code.add_line("extend_result = result.extend")
        code.add_line("to_str = str")
        return code

    def compiler(self):
        self.tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", self.text)
        for token in self.tokens:
            if token.startswith('{#'):
                continue
            elif token.startswith('{{'):
                expr = self._expr_code(token[2:-2].strip())
                self.buffered.append("to_str(%s)" % expr)
            elif token.startswith('{%'):
                self.flush_output()
                words = token[2:-2].strip().split()
                if words[0] == 'if':
                    if len(words) != 2:
                        self._syntax_error("Don't understand if", token)
                    self.ops_stack.append('if')
                    self.code.add_line("if %s:" % self._expr_code(words[1]))
                    self.code.indent()
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    self.ops_stack.append('for')
                    self._variable(words[1], self.loop_vars)
                    self.code.add_line(
                        "for c_%s in %s:" % (
                            words[1],
                            self._expr_code(words[3])
                        )
                    )
                    self.code.indent()
                elif words[0].startswith('end'):
                    if len(words) != 1:
                        self._syntax_error("Don't understand end", token)
                    end_what = words[0][3:]
                    if not self.ops_stack:
                        self._syntax_error("Too many ends", token)
                    start_what = self.ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error("Mismatched end tag", end_what)
                    self.code.dedent()
                else:
                    self._syntax_error("Don't understand tag", words[0])
            else:
                if token:
                    self.buffered.append(repr(token))

        if self.ops_stack:
            self._syntax_error("Unmatched action tag", self.ops_stack[-1])

        self.flush_output()

        for var_name in self.all_vars - self.loop_vars:
            self.vars_code.add_line("c_%s = context[%r]" % (var_name, var_name))

        self.code.add_line("return ''.join(result)")
        self.code.dedent()
        self._render_function = self.code.get_globals()['render_function']

    def flush_output(self):
        """Force `buffered` to the code builder."""
        if len(self.buffered) == 1:
            self.code.add_line("append_result(%s)" % self.buffered[0])
        elif len(self.buffered) > 1:
            self.code.add_line("extend_result([%s])" % ", ".join(self.buffered))
        del self.buffered[:]

    def _expr_code(self, expr):
        if "|" in expr:
            pipes = expr.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_vars)
                code = "c_%s(%s)" % (func, code)
        elif "." in expr:
            dots = expr.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])
            code = "do_dots(%s, %s)" % (code, args)
        else:
            self._variable(expr, self.all_vars)
            code = "c_%s" % expr
        return code

    def _syntax_error(self, msg, thing):
        raise TempliteSyntaxError("%s: %r" % (msg, thing))

    def _variable(self, name, vars_set):
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            self._syntax_error("Not a valid name", name)
        vars_set.add(name)

    def render(self, context=None):
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def _do_dots(self, value, *dots):
        """Evaluate dotted expressions at runtime."""
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value
