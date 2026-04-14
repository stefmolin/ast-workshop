"""The final state of the ImportVisitor after completing exercise 7."""

import ast
import builtins
from collections import defaultdict


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, source_code: str) -> None:
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
            and name
            == (import_info['alias'] or import_info['import'])
        ]

        if not scoped_imports:
            return None

        return max(
            scoped_imports, key=lambda x: x['scope'].count('.')
        )

    def _flag_if_masked(self, name):
        if len(definitions := self.names_defined[name]) < 2:
            return

        latest_def = definitions[-1]

        # mark all others still in scope as masked
        for older_def in definitions[:-1]:
            if self._is_in_scope(older_def['scope']):
                older_line = (
                    f' on line {older_def["line_number"]}'
                    if older_def['line_number'] is not None
                    else ''
                )  # empty for builtins only
                print(
                    f'{older_def["type"]} {name}{older_line}',
                    f'is masked by the {latest_def["type"]}',
                    'of the same name',
                    f'on line {latest_def["line_number"]}',
                )

    def _track_name_definition(self, node, name):
        self.names_defined[name].append(
            {
                'scope': '.'.join(self.stack),
                'type': node.__class__.__name__,
                'line_number': node.lineno,
            }
        )
        self._flag_if_masked(name)

    def _visit_import(self, node):
        import_scope = '.'.join(self.stack)
        self.imports_available.extend(
            [
                {
                    'scope': import_scope,
                    'import': alias.name,
                    'from': getattr(node, 'module', None),
                    'alias': alias.asname,
                    'times_accessed': 0,
                    'line_number': node.lineno,
                }
                for alias in node.names
                if alias.name != '*'
            ]
        )
        for alias in node.names:
            self._track_name_definition(
                node, alias.asname or alias.name
            )
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self._track_name_definition(node, node.id)

        elif isinstance(node.ctx, ast.Load):
            if not (
                any(
                    self._is_in_scope(name_info['scope'])
                    for name_info in self.names_defined[node.id]
                )
            ):
                print(
                    f'Missing definition for {node.id}',
                    f'on line {node.lineno}',
                )

            elif import_of_name := self.get_in_scope_import(
                node.id
            ):
                import_of_name['times_accessed'] += 1

        self.generic_visit(node)

    def generic_visit(self, node):
        if hasattr(node, 'body'):
            # we have entered a new scope
            self.stack.append(getattr(node, 'name', 'module'))
        super().generic_visit(node)
        if hasattr(node, 'body'):
            self.stack.pop()

    def visit(self, node):
        if isinstance(node, ast.Import | ast.ImportFrom):
            self._visit_import(node)
        elif isinstance(
            node,
            ast.ClassDef
            | ast.FunctionDef
            | ast.AsyncFunctionDef
            | ast.arg,
        ):
            self._track_name_definition(
                node,
                node.arg
                if isinstance(node, ast.arg)
                else node.name,
            )
            self.generic_visit(node)
        else:
            super().visit(node)

    def run(self):
        self.visit(self.tree)
        for import_info in self.imports_available:
            if not import_info['times_accessed']:
                print(
                    f'Unused import {import_info["import"]}',
                    f'on line {import_info["line_number"]}',
                )


if __name__ == '__main__':
    from textwrap import dedent

    source_code = dedent(r"""
    import json
    import re
    import z

    def dict(): ...

    def test(ast, json):
        import ast
        class ast: ...
        return ast

    def json():
        x = re.compile('x')
        with contextlib.suppress(KeyError):
            del x['key']

    def test_two():
        x = contextlib = dict()
        with contextlib.suppress(KeyError):
            del x['key']
    """).strip()

    print(
        'Source code input:',
        source_code,
        'Running linter...',
        sep='\n',
    )

    visitor = ImportVisitor(source_code)
    visitor.run()
