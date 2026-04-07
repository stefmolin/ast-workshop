"""
ImportVisitor starting point for exercise 5

The `if __name__ == '__main__'` section below will run the traversal on some sample
source code (also defined there). You can test your changes by modifying that section
to include some checks of your changes and then running this script.
"""

import ast


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.imports_available = []
        self.stack = []

    def _is_in_scope(self, definition_scope: str) -> bool:
        pass

    def get_in_scope_import(self, name: str) -> dict | None:
        pass

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
                if alias.name != '*'
            ]
        )
        self.generic_visit(node)

    def visit_Import(self, node):
        self._visit_import(node)

    def visit_ImportFrom(self, node):
        self._visit_import(node)

    def generic_visit(self, node):
        if hasattr(node, 'body'):
            self.stack.append(getattr(node, 'name', 'module'))
        super().generic_visit(node)
        if hasattr(node, 'body'):
            self.stack.pop()

    def run(self):
        self.visit(self.tree)


if __name__ == '__main__':
    import pprint
    from textwrap import dedent

    source_code = dedent(r"""
    import re
    import pandas as pd

    def strip_password(x1: dict[str, str]) -> None:
        with contextlib.suppress(KeyError):
            del x1['password']
        a = re.compile(r'\w+')

    def strip_password_two(x2: dict[str, str]) -> None:
        from contextlib import suppress
        with suppress(KeyError):
            del x2['password']
        a = pd.DataFrame()

    def strip_password_three(x3: dict[str, str]) -> None:
        with suppress(KeyError):
            del x3['password']

    def strip_password_three(x4: dict[str, str]) -> None:
        import contextlib
        with contextlib.suppress(KeyError):
            del x4['password']
    """)

    print(
        'Source code input:',
        source_code,
        'Running linter...',
        sep='\n',
    )

    visitor = ImportVisitor(source_code)
    visitor.run()

    print('Found the following imports:')
    pprint.pprint(visitor.imports_available)

    # TIP: add dummy stack for testing now that imports are processed
    # visitor.stack = ['module', 'strip_password_three']

    # you can change the value you pass in here to test the result based on your stack
    # print(visitor.get_in_scope_import('contextlib'))

    # same thing here
    # print(visitor._is_in_scope('module'))
