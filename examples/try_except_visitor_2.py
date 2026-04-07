import ast


class TryExceptVisitor(ast.NodeVisitor):
    def visit_Try(self, node):
        if len(node.handlers) == 1 and isinstance(
            node.handlers[0].body[-1], ast.Pass
        ):
            print(
                'try/except/pass block on line',
                f'{node.lineno}, use contextlib.suppress',
            )
        self.generic_visit(node)


if __name__ == '__main__':
    from pathlib import Path

    EXAMPLES_DIR = Path(__file__).parent
    WORKSHOP_DIR = EXAMPLES_DIR.parent
    SNIPPETS_DIR = WORKSHOP_DIR / 'snippets'

    for snippet in ['try_except.py', 'try_except_nested.py']:
        print(f'\nRunning for {snippet=}:')
        source_code = (SNIPPETS_DIR / snippet).read_text()
        print(source_code)

        tree = ast.parse(source_code)
        visitor = TryExceptVisitor()
        visitor.visit(tree)

        print('---')
