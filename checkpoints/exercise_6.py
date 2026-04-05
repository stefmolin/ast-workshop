"""
ImportVisitor starting point for exercise 6

The `if __name__ == '__main__'` section below will run the traversal on some sample
source code (also defined there). You can test your changes by modifying that section
to include some checks of your changes and then running this script.
"""

import ast
import builtins
from collections import defaultdict


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.stack = []
        self.imports_available = []
        self.names_defined = defaultdict(list)

        for builtin in builtins.__dict__.keys():
            self.names_defined[builtin].append(
                {
                    'scope': 'module',
                    'type': 'builtin',
                    'line_number': None,
                }
            )

    def _is_in_scope(self, definition_scope):
        check_scope = definition_scope.split('.')
        return self.stack[: len(check_scope)] == check_scope

    def get_in_scope_import(self, name):
        scoped_imports = [
            import_info
            for import_info in self.imports_available
            if self._is_in_scope(import_info['scope'])
            and name == (import_info['alias'] or import_info['import'])
        ]

        if not scoped_imports:
            return None

        return max(scoped_imports, key=lambda x: x['scope'].count('.'))

    def _visit_import(self, node):
        import_scope = '.'.join(self.stack)
        self.imports_available.extend(
            [
                {
                    'scope': import_scope,
                    'import': alias.name,
                    'from': getattr(node, 'module', None),
                    'alias': alias.asname,
                }
                for alias in node.names
                if alias.name != '*'  # not handling this special case
            ]
        )
        self.generic_visit(node)

    def visit_Import(self, node):
        self._visit_import(node)

    def visit_ImportFrom(self, node):
        self._visit_import(node)

    def generic_visit(self, node):
        if hasattr(node, 'body'):
            # we have entered a new scope
            self.stack.append(getattr(node, 'name', 'module'))
        super().generic_visit(node)
        if hasattr(node, 'body'):
            self.stack.pop()

    def run(self):
        self.visit(self.tree)


if __name__ == '__main__':
    from textwrap import dedent

    source_code = dedent(r"""
    import json

    def dict(): ...

    def test(ast, json):
        import ast
        class ast: ...
        return ast

    def json():
        x = {}
        with contextlib.suppress(KeyError):
            del x['key']
    """).strip()
    visitor = ImportVisitor(source_code)
    visitor.run()
