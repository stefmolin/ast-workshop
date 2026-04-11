import ast
from textwrap import dedent


class TryExceptTransformer(ast.NodeTransformer):
    def __init__(self, source_code):
        self.tree = ast.parse(source_code)
        self.has_changed = False

    def _get_suppress_block(self, node):
        suppress_example = dedent("""
        with contextlib.suppress(Exception):
            pass
        """)
        with_block = ast.parse(suppress_example).body[0]

        if exc_type := node.handlers[0].type:
            with_block.items[0].context_expr.args = [exc_type]

        with_block.body = node.body

        return with_block

    def visit_Try(self, node):
        if len(node.handlers) == 1 and isinstance(
            node.handlers[0].body[-1], ast.Pass
        ):
            print(
                'Detected a try/except/pass block on',
                f'line {node.lineno}, rewriting',
            )
            self.has_changed = True
            node = self._get_suppress_block(node)
        self.generic_visit(node)
        return node

    def run(self):
        self.tree = self.visit(self.tree)
        if self.has_changed:
            self.tree.body = [
                ast.Import([ast.alias('contextlib')])
            ] + self.tree.body
        return ast.fix_missing_locations(self.tree)


if __name__ == '__main__':
    from pathlib import Path

    EXAMPLES_DIR = Path(__file__).parent
    WORKSHOP_DIR = EXAMPLES_DIR.parent
    SNIPPETS_DIR = WORKSHOP_DIR / 'snippets'

    source_code = (SNIPPETS_DIR / 'try_except.py').read_text()
    transformer = TryExceptTransformer(source_code)
    updated_ast = transformer.run()
    print(ast.unparse(updated_ast))
