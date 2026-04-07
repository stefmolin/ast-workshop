"""The initial state of the ImportVisitor after it is first introduced."""

import ast


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.imports_available = []

    def _visit_import(self, node):
        self.imports_available.extend(
            [
                {
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

    def run(self):
        self.visit(self.tree)


if __name__ == '__main__':
    import pprint
    from pathlib import Path

    CHECKPOINTS_DIR = Path(__file__).parent
    WORKSHOP_DIR = CHECKPOINTS_DIR.parent
    SNIPPETS_DIR = WORKSHOP_DIR / 'snippets'

    source_code = (SNIPPETS_DIR / 'imports.py').read_text()
    visitor = ImportVisitor(source_code)
    visitor.run()

    print('Found the following imports:')
    pprint.pprint(visitor.imports_available)
