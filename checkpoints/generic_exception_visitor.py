import ast
from textwrap import dedent, indent


class GenericExceptionVisitor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)

    def _print_source_segment(self, node):
        code_segment = ast.get_source_segment(
            self.source_code, node, padded=True
        )
        print(indent(dedent(code_segment), '| '), end='\n\n')

    def visit_Raise(self, node):
        if (
            (
                isinstance(node.exc, ast.Name)
                and node.exc.id == 'Exception'
            )
            or (
                isinstance(node.exc, ast.Call)
                and node.exc.func.id == 'Exception'
            )
        ):
            print(
                'Generic Exception raised on line',
                f'{node.lineno}:'
            )
            self._print_source_segment(node)

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if not (exception_type := node.type):
            print(f'Bare except on line {node.lineno}:')
            self._print_source_segment(node)

        elif exception_type.id == 'Exception':
            print(f'Generic Exception on line {node.lineno}:')
            self._print_source_segment(node)

        self.generic_visit(node)

    def run(self):
        self.visit(self.tree)