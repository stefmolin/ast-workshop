import ast


class AssertTransformer(ast.NodeTransformer):
    def visit_Assert(self, node):
        if not node.msg:
            node.msg = ast.Constant('TODO: Add failure info')
            ast.fix_missing_locations(node)
        return self.generic_visit(node)


if __name__ == '__main__':
    from pathlib import Path

    EXAMPLES_DIR = Path(__file__).parent
    WORKSHOP_DIR = EXAMPLES_DIR.parent
    SNIPPETS_DIR = WORKSHOP_DIR / 'snippets'

    source_code = (SNIPPETS_DIR / 'assert.py').read_text()
    tree = ast.parse(source_code)

    transformer = AssertTransformer()
    updated_ast = transformer.visit(tree)

    print(
        'Transformed code:', ast.unparse(updated_ast), sep='\n'
    )
