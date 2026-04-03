---
title: Process, Analyze, and Transform Python Code with ASTs
author: Stefanie Molin
description: In this workshop, Stefanie Molin teaches you how to use abstract syntax trees (ASTs) to process, analyze, and transform Python code. Using just the standard library, we will implement a couple of common checks from scratch, which will give you an idea of how these tools work and help you build the skills and confidence to use ASTs in your own projects.
published: "2026-04-11T00:00:00.000-04:00"
g_tag: G-25389D1SR4
keywords: [ast, abstract-syntax-tree, python]
og:
  image: # TODO
    url: https://stefaniemolin.com/build-your-own-simple-static-code-analyzer-talk/media/traversal-animation.gif
    width: 1368
    height: 1079
    alt: Animation of AST traversal in Python on a simple module with a class and two methods.
  locale: en_US
  site_name: Stefanie Molin
  title: "{title} | {author}"
  type: website
  url: https://stefaniemolin.com/ast-workshop
twitter:
  card: summary
  site: "@StefanieMolin"
  creator: "@StefanieMolin"
page_title: "{title} slides | {author}"
rel_me:
  - https://github.com/stefmolin
  - https://linkedin.com/in/stefanie-molin/
  - https://x.com/StefanieMolin
  - https://bsky.app/profile/stefaniemolin.com
license:
  name: CC BY-NC-SA 4.0
  link: https://creativecommons.org/licenses/by-nc-sa/4.0/
website: stefaniemolin.com
favicon: /favicon
intro_slide:
  title: Process, Analyze, and Transform Python Code with ASTs
reveal:
  version: 5.2.1
  theme: simple
  config:
    controls: false
    hash: true
    history: true
    pdfSeparateFragments: false
    slideNumber: c/t # TODO: decide on this
highlightjs:
  version: 11.11.1
  theme: stackoverflow-light
fontawesome:
  version: 7.0.1
thank_you_slide: ../thank-you-slide/thank-you.html
# TODO: need to add the exercise timer
---

[id=bio]
## Bio

- 👩🏻‍💻 Software engineer at Bloomberg in NYC
- ✨ Core developer of [numpydoc](https://github.com/numpy/numpydoc) and creator of [numpydoc's pre-commit hook](https://numpydoc.readthedocs.io/en/latest/validation.html#docstring-validation-using-pre-commit-hook), which uses ASTs
- ✍ Author of "[Hands-On Data Analysis with Pandas](https://stefaniemolin.com/books/Hands-On-Data-Analysis-with-Pandas-2nd-edition/)"
- 🎓 Bachelor's degree in operations research from Columbia University
- 🎓 Master's degree in computer science from Georgia Tech

---

[id=ast-definition]
## Abstract Syntax Tree (AST)

<ul>
  <li class="fragment fade-in">
    Represents the structure of the source code as a tree
  </li>
  <li class="fragment fade-in">
    Nodes in the tree are language constructs (<em>e.g.</em>, module, class, function)
  </li>
  <li class="fragment fade-in">
    Each node has a single parent (<em>e.g.</em>, a class is a child of a single module)
  </li>
  <li class="fragment fade-in">
    Parent nodes can have multiple children (<em>e.g.</em>, a class can have several methods)
  </li>
</ul>

---

[data-transition=slide-in fade-out,id=greeter-snippet]

Let's see what this code snippet (`greet.py`) looks like when represented as an AST:

```python
class Greeter:
    def __init__(self, enthusiasm: int = 1) -> None:
        self.enthusiasm = enthusiasm

    def greet(self, name: str = 'World') -> str:
        return f'Hello, {name}{"!" * self.enthusiasm}'
```

---

[data-transition=slide-out fade-in,id=greeter-snippet-ast]
<div class="center">
  <img width="650" src="media/full-ast.svg" alt="The AST for greet.py visualized with Graphviz">
  <br/>
  <small>The AST for <code>greet.py</code> visualized with Graphviz.</small>
</div>

---

### Popular open source tools that use ASTs

<ul>
  <li class="fragment fade-in">
    Linters and formatters, like <code>ruff</code> (Rust) and <code>black</code> (Python)
  </li>
  <li class="fragment fade-in">
    Documentation tools, like <code>sphinx</code> and the <code>numpydoc-validation</code> pre-commit hook
  </li>
  <li class="fragment fade-in">
    Automatic Python syntax upgrade tools, like <code>pyupgrade</code>
  </li>
  <li class="fragment fade-in">
    Next-generation notebooks, like <code>marimo</code>
  </li>
  <li class="fragment fade-in">
    Type checkers, like <code>mypy</code>
  </li>
  <li class="fragment fade-in">
    Code security tools, like <code>bandit</code>
  </li>
  <li class="fragment fade-in">
    Code and testing coverage tools, like <code>vulture</code> and <code>coverage.py</code>
  </li>
  <li class="fragment fade-in">
    Testing frameworks that instrument your code or generate tests based on it, like <code>hypothesis</code> and <code>pytest</code>
  </li>
</ul>

[notes]
Other potential use cases:

- Metaprogramming
- Updating syntax after upgrading dependency
- Analyzing code structure
- Forbidding certain imports or types of imports (like not allowing relative imports or `import *`)

---

[id=asts-in-python]
## ASTs in Python

<ul>
  <li class="fragment fade-in">
    Represent syntactically-correct Python code (cannot be generated in the presence of syntax errors)
  </li>
  <li class="fragment fade-in">
    Created by the parser as an intermediary step when
    <a href="https://github.com/python/cpython/blob/main/InternalDocs/compiler.md">
      compiling source code into byte code
    </a> (necessary to run it)
  </li>
  <li class="fragment fade-in">
    Available in the standard library via the <code>ast</code> module
  </li>
</ul>

---

[id=parsing-python-source-code-into-an-ast]
### Parsing Python source code into an AST

---

[id=read-in-the-source-code]
#### 1. Read in the source code

```pycon
>>> from pathlib import Path
>>> source_code = Path('greet.py').read_text()
```

---

[id=parse-source-code-with-the-ast-module]
#### 2. Parse it with the `ast` module

If the code is syntactically-correct, we get an AST back:

```pycon
>>> import ast
>>> tree = ast.parse(source_code)
>>> print(type(tree))
<class 'ast.Module'>
```

---

[id=inspecting-the-ast]
### Inspecting the AST

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    We can use the <code>ast.dump()</code> function to display the AST:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    The root node is an <code>ast.Module</code> node:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    It contains everything else in its <code>body</code> attribute:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    The <code>greet.py</code> file first defines a class, named <code>Greeter</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    The <code>ast.ClassDef</code> node also contains the <code>body</code> of the <code>Greeter</code> class:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    The first entry is the <code>Greeter.__init__()</code> method:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="5">
    The <code>ast.FunctionDef</code> node includes information about the arguments:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="6">
    Its <code>body</code> contains the AST representation of the function's code:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="7">
    The return annotation is stored in the <code>returns</code> attribute:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="8">
    The final entry is the <code>Greeter.greet()</code> method:
  </p>
</div>

<pre>
    <code data-trim class="language-pycon hide-line-numbers" data-line-numbers="1|2|3-51|4-5|6-53|7-8|9-16|17-24|25|26-53" data-fragment-index="0">
>>> print(ast.dump(tree, indent=2))
Module(
  body=[
    ClassDef(
      name='Greeter',
      body=[
        FunctionDef(
          name='__init__',
          args=arguments(
            args=[
              arg(arg='self'),
              arg(
                arg='enthusiasm',
                annotation=Name(id='int', ctx=Load()))],
            defaults=[
              Constant(value=1)]),
          body=[
            Assign(
              targets=[
                Attribute(
                  value=Name(id='self', ctx=Load()),
                  attr='enthusiasm',
                  ctx=Store())],
              value=Name(id='enthusiasm', ctx=Load()))],
          returns=Constant(value=None)),
        FunctionDef(
          name='greet',
          args=arguments(
            args=[
              arg(arg='self'),
              arg(
                arg='name',
                annotation=Name(id='str', ctx=Load()))],
            defaults=[
              Constant(value='World')]),
          body=[
            Return(
              value=JoinedStr(
                values=[
                  Constant(value='Hello, '),
                  FormattedValue(
                    value=Name(id='name', ctx=Load()),
                    conversion=-1),
                  FormattedValue(
                    value=BinOp(
                      left=Constant(value='!'),
                      op=Mult(),
                      right=Attribute(
                        value=Name(id='self', ctx=Load()),
                        attr='enthusiasm',
                        ctx=Load())),
                    conversion=-1)]))],
          returns=Name(id='str', ctx=Load()))])])
</code>
</pre>

---

[id=exercise-1]
### Exercise

Try passing source code that has a `SyntaxError` into `ast.parse()`. What happens? What about if the code has an error unrelated to syntax, like a `NameError` or `TypeError`?

---

[id=example-solution-1]
### Example solution

#### Syntactically-incorrect source code

Let's use the following malformed `import` statement as an example of **invalid source code**:

```pycon
>>> import timedelta from datetime
  File "<stdin>", line 1
    import timedelta from datetime
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: Did you mean to use 'from ... import ...' instead?
```

---

We also encounter a `SyntaxError` when attempting to parse this into an AST:

```pycon [highlight-lines="1-2,14"][class="hide-line-numbers"]
>>> import ast
>>> tree = ast.parse('import timedelta from datetime')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    ast.parse('import timedelta from datetime')
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../ast.py", line 46, in parse
    return compile(source, filename, mode, flags,
                   _feature_version=feature_version,
                   optimize=optimize)
  File "<unknown>", line 1
    ast.parse('import timedelta from datetime')
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: Did you mean to use 'from ... import ...' instead?
```

---

#### Syntactically-correct source code with logic errors

The following code raises a `NameError` at runtime:

```pycon
>>> a + 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    a + 5
    ^
NameError: name 'a' is not defined
```

<div class="fragment">

<p>However, it is syntactically-correct, so we can parse it into an AST:<p>

```pycon
>>> ast.parse('a + 5')
Module(body=[Expr(value=BinOp(...))], type_ignores=[])
```

</div>

---

## Working with ASTs

In addition to being a highly-nested structure, attributes containing nodes may be named differently across node types. To see this, let's take a look at the AST for the following snippet in `assert.py`:

```python
def duplicate_list(x):
    assert isinstance(x, list)
    return x + x
```

---

[data-transition=slide-out fade-in]
<div class="center">
  <img width="450" src="media/assert-ast-attributes.svg" alt="The AST for assert.py visualized with Graphviz">
  <br/>
  <small>The AST for <code>assert.py</code> with node attributes visualized with Graphviz.</small>
</div>

---

### Traversing the AST

To effectively analyze code using the AST, we need to traverse it and inspect the nodes we care about. Depending on how much of the tree we want to explore and how much context we need about each node, there are different approaches. Let's walk through the different ways using the `assert.py` example:

```python
import ast
from pathlib import Path

source_code = Path('snippets/assert.py').read_text()
tree = ast.parse(source_code)
```

---

#### `ast.iter_fields()`

We can use the `ast.iter_fields()` function to iterate over all fields that a node has. Our AST is rooted at an `ast.Module` node, so there isn't much here:

```pycon
>>> print(list(ast.iter_fields(tree)))
[('body', [<ast.FunctionDef at 0x1086bea10>]),
 ('type_ignores', [])]
```

---

If we look at this for the `ast.FunctionDef` in the `body` of the `ast.Module`, we have more information:

```pycon
>>> func_def = tree.body[0]
>>> print(list(ast.iter_fields(func_def)))
[('name', 'duplicate_list'),
 ('args', <ast.arguments at 0x1085794e0>),
 ('body', [<ast.Assert at 0x10884d6c0>,
           <ast.Return at 0x10884d9f0>]),
 ('decorator_list', []),
 ('returns', None),
 ('type_comment', None)]
```

---

#### `ast.iter_child_nodes()`

The `ast.iter_fields()` function is helpful when figuring out how to work with individual node types. The `ast.iter_child_nodes()` builds on top of this to traverse the tree starting at a given node. It yields all nodes it encounters along the way that are direct children of the starting node (they can be in any field, but they cannot be grandchildren, like the children of the `ast.Assert` node below):

```pycon
>>> print(list(ast.iter_child_nodes(func_def)))
[<ast.arguments at 0x1085794e0>,
 <ast.Assert at 0x10884d6c0>,
 <ast.Return at 0x10884d9f0>]
```

---

To traverse the entire tree, we need the recursive behavior provided in the `ast.walk()` function or the `ast.NodeVisitor`/`ast.NodeTransformer` classes. Each of these builds upon the `ast.iter_fields()` and `ast.iter_child_nodes()` functions we just looked at. Let's start with the `ast.walk()` function

---

#### `ast.walk()`

The `ast.walk()` function recursively yields all descendant nodes in the AST. Let's use it to make sure all `assert` calls provide a message when the `assert` is false and an `AssertionError` is raised. For those unfamiliar with the syntax, here's a comparison using the contents of `assert.py`:

```python
# without custom message
def duplicate_list(x):
    assert isinstance(x, list)
    return x + x

# with custom message
def duplicate_list(x):
    assert isinstance(x, list), 'Input is not a list'
    return x + x
```

---

##### Modifying code before running it with `ast.walk()`

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    The <code>ast.walk()</code> function yields all nodes descending from <code>tree</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    We want to modify all <code>ast.Assert</code> nodes that do not have a message (<code>msg</code>):
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    We set the <code>msg</code> to a placeholder value, so it's easy to find in the logs:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    All nodes to must have line numbers in order to compile the AST into a <code>code</code> object:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    The <code>compile()</code> function turns our modified AST into a <code>code</code> object:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    We can execute <code>code</code> objects with the <code>exec()</code> function:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="5">
    This runs the function definition for <code>duplicate_list()</code>, so we can now call it:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="6">
    The input we passed fails the <code>assert</code>, raising an <code>AssertionError</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="7">
    Notice that we get the message we injected when we modified the AST:
  </p>
</div>

<pre>
    <code data-trim class="language-pycon hide-line-numbers" data-line-numbers="1|2|3|4|6|7|8|9-14|3,14" data-fragment-index="0">
>>> for node in ast.walk(tree):
...     if isinstance(node, ast.Assert) and not node.msg:
...         node.msg = ast.Constant('TODO: Add failure info')
...         ast.fix_missing_locations(node)
>>>
>>> code = compile(tree, '&lt;ast_workshop&gt;', 'exec')
>>> exec(code)
>>> duplicate_list(1)
Traceback (most recent call last):
  File "&lt;stdin&gt;", line 1, in &lt;module&gt;
    duplicate_list(1)
    ~~~~~~~~~~~~~~^^^
  File "&lt;ast_workshop&gt;", line 3, in duplicate_list
AssertionError: TODO: Add failure info
</code></pre>

---

##### Can we convert this back into source code to save it?

With a small example like this, we can also use the `ast.unparse()` function to convert the modified AST back into Python source code:

```pycon [highlight-lines="1|2-4|3"][class="hide-line-numbers"]
>>> print(ast.unparse(tree))
def duplicate_list(x):
    assert isinstance(x, list), 'TODO: Add failure info'
    return x + x
```

---

The `ast.unparse()` function comes with some caveats:

<ul>
    <li class="fragment">It's not recommended with larger trees since it can hit recursion limits.</li>
    <li class="fragment">If we first convert source code to an AST, and then attempt to convert it back without an changes, the result will be <em>equivalent, but not necessarily equal</em> to the original.</li>
</ul>

---

One way that the round-trip could result in equivalent, but different source code is in the presence of non-code elements like comments and stylistic formatting. These aren't part of the AST because they don't they have no effect on the logic of the program. For example, if we try to round-trip this code:

```python
import contextlib


def strip_password(
    credentials: dict[str, str]
) -> None:
    '''
    Strip out the password from the credentials.
    '''

    # remove the password if it is there
    with contextlib.suppress(KeyError):
        del credentials["password"]
```

---

When we parse this into an AST and back again, the code is equivalent, but different:

```python
import contextlib

def strip_password(credentials: dict[str, str]) -> None:
    """
    Strip out the password from the credentials.
    """
    with contextlib.suppress(KeyError):
        del credentials['password']
```

---

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    There are no longer two blank lines after the import:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    The function definition is now written entirely on one line:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    The docstring now uses <code>"""</code> instead of <code>'''</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    There is no longer a blank line between the docstring and the code:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    The comment has been removed:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    Single quotes are used for keying into the dictionary:
  </p>
</div>

<div>
<pre>
    <code data-trim class="language-diff hide-line-numbers" data-line-numbers="1-3|4-7|8-12|12-13|14|16-17" data-fragment-index="0">

  import contextlib

-
- def strip_password(
+ def strip_password(credentials: dict[str, str]) -> None:
-     credentials: dict[str, str]
- ) -> None:
-     '''
+     """
      Strip out the password from the credentials.
-     '''
+     """
-
-     # remove the password if it is there
      with contextlib.suppress(KeyError):
-         del credentials["password"]
+         del credentials['password']
    </code>
</pre>
</div>

---

[id=exercise-2]
### Exercise

Use the `ast.walk()` function and the `ast.get_docstring()` function to traverse the AST for `greet.py` and report any items that are missing docstrings.

---

[id=example-solution-2]
### Example solution

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    Similar setup to the previous examples, except we also import <code>contextlib</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    Multiple node types can have docstrings, so we don't limit to a type here:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    We try to access each node's docstring and <code>suppress</code> any <code>TypeErrors</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    If there isn't a docstring, we report it along with the node's name:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    The module, <code>Greeter</code> class, and the <code>Greeter</code> class's methods lack docstrings:
  </p>
</div>

<div>
<pre>
    <code data-trim class="language-python hide-line-numbers" data-line-numbers="1-3,5|6-9|2,7|8-9|10-13" data-fragment-index="0">
>>> import ast
>>> import contextlib
>>> from pathlib import Path
>>>
>>> tree = ast.parse(Path('snippets/greet.py').read_text())
>>> for node in ast.walk(tree):
...    with contextlib.suppress(TypeError):
...        if not ast.get_docstring(node):
...            print(getattr(node, 'name', 'module'))
module
Greeter
__init__
greet
</code></pre>

---

The `ast.walk()` function yields the nodes in no specific order, so we don't have context beyond the node itself. In the case of the previous exercise, larger files can easily make the results confusing. Furthermore, we may want to flag missing docstrings on the `__init__()` method only if the class doesn't have one. For these use cases, we need the context provided by traversing the tree in a specific order.

---

### Depth-first traversal

The `ast` module provides two classes that for depth-first traversal of an AST:

<ul>
    <li class="fragment"><code>ast.NodeVisitor</code>: visits nodes in an AST</li>
    <li class="fragment"><code>ast.NodeTransformer</code>: special version of the above that can also modify nodes</li>
</ul>

---

Suppose we want to check our code for the `try`/`except`/`pass` anti-pattern like the following code from `try_except.py`:

```python
def strip_password(x: dict[str, str]) -> None:
    try:
        del x['password']
    except KeyError:
        pass
```

<div class="fragment">

<p>Instead, we want to encourage the use of <code>contextlib.suppress()</code>:</p>

```python
import contextlib

def strip_password(x: dict[str, str]) -> None:
    with contextlib.suppress(KeyError):
        del x['password']
```

</div>

---

#### `ast.NodeVisitor`

When we subclass `ast.NodeVisitor`, we create `visit_<NodeType>()` methods for each AST node we want to visit and the `ast.NodeVisitor` will take care of calling them as nodes of that type are encountered.

---

We need to visit each `ast.Try` node and inspect its `handlers` &ndash; if there is only one handler and its `body` is an `ast.Pass` node then we will report it:

```python
class TryExceptVisitor(ast.NodeVisitor):

    def visit_Try(self, node):
        if (
            len(node.handlers) == 1
            and isinstance(node.handlers[0].body[-1], ast.Pass)
        ):
            print(
                'try/except/pass block on line',
                f'{node.lineno}, use contextlib.suppress',
            )
```

---

To use our visitor, we instantiate it and call its `visit()` method, passing in the AST, to start the traversal:

```pycon [highlight-lines="1-5|3|4|5"][class="hide-line-numbers"]
>>> source_code = Path('snippets/try_except.py').read_text()
>>> tree = ast.parse(source_code)
>>> visitor = TryExceptVisitor()
>>> visitor.visit(tree)
try/except/pass block on line 3, use contextlib.suppress
```

---

We aren't done yet though. The `visit_Try()` method is currently cutting off the traversal to descendants of `ast.Try` nodes, meaning our visitor never visits nested `try` blocks (only the outermost one). Consider this example of nested `try` blocks from `try_except_nested.py`, where we want to detect the anti-pattern in the inner `try`:

```python [highlight-lines="1-9|4-7"][class="hide-line-numbers"]
def strip_password(x: dict[str, str]) -> None:
    try:
        print(f'Received dict with keys: {x.keys()}')
        try:
            del x['password']
        except KeyError:
            pass
    except Exception as e:
        raise TypeError('Invalid input, expected dict') from e
```

---

The `TryExceptVisitor` doesn't find anything with this input because it doesn't go any deeper after it visits the outermost `try`:

```pycon
>>> source_code = Path('snippets/try_except_nested.py')
>>> tree = ast.parse(source_code.read_text())
>>> visitor = TryExceptVisitor()
>>> visitor.visit(tree)
```

---

[data-transition=slide-out fade-in]
<div class="center">
  <img width="300" src="media/animation-try-except-nested-blocked.gif" alt="Partial AST traversal of try_except_nested.py with the initial TryExceptVisitor visualized with Graphviz">
  <br/>
  <small>Partial AST traversal of <code>try_except_nested.py</code> with the initial <code>TryExceptVisitor</code> visualized with Graphviz.</small>
</div>

---

##### The `generic_visit()` method

When we don't define a dedicated `visit_<NodeType>()` method for an AST node, the `ast.NodeVisitor` calls the `generic_visit()` method, which continues the traversal. The `visit_Try()` method we defined does not currently call `generic_visit()` on that node, so the traversal does not go any deeper.

---

We need to call `generic_visit()` ourselves. Note the indentation level &ndash; it is outside of the `if` because we want to visit all nodes, regardless of whether their ancestors had the issue we are looking for:

```python [highlight-lines="12"][class="hide-line-numbers"]
class TryExceptVisitor(ast.NodeVisitor):

    def visit_Try(self, node):
        if (
            len(node.handlers) == 1
            and isinstance(node.handlers[0].body[-1], ast.Pass)
        ):
            print(
                'try/except/pass block on line',
                f'{node.lineno}, use contextlib.suppress',
            )
        self.generic_visit(node)
```

---

The `TryExceptVisitor` now visits the innermost `try` and detects the issue:

```pycon [highlight-lines="5"][class="hide-line-numbers"]
>>> source_code = Path('snippets/try_except_nested.py')
>>> tree = ast.parse(source_code.read_text())
>>> visitor = TryExceptVisitor()
>>> visitor.visit(tree)
try/except/pass block on line 5, use contextlib.suppress
```

---

[data-transition=slide-out fade-in]
<div class="center">
  <img width="700" src="media/animation-try-except-nested-full.gif" alt="Full AST traversal of try_except_nested.py visualized with Graphviz">
  <br/>
  <small>Full AST traversal of <code>try_except_nested.py</code> visualized with Graphviz.</small>
</div>

---

[id=exercise-3]
### Exercise

Create a `GenericExceptionVisitor` class that detects both bare `except` blocks and usage of generic `Exceptions`. Your visitor will need to visit both `ast.Raise` and `ast.ExceptionHandler` nodes. You can test it using the source code in `generic_exception.py`:

```python
try:
    del x['non_existent_key']
except:  # bare except
    raise Exception('No such key')  # generic Exception
```

**Bonus**: If you have time, use the `ast.get_source_segment()` function to print any problematic code you detect.

---

[id=example-solution-3]
### Example solution


<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    In addition to <code>ast</code>, we will also use <code>textwrap</code> for text formatting:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    We start by inheriting from <code>ast.NodeVisitor</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    In order to use <code>ast.get_source_segment()</code>, we need the source code string:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    <code>_print_source_segment()</code> will print the source code we reference:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    <code>ast.get_source_segment()</code> needs the full source code and the AST node:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    <code>visit_Raise()</code> defines our actions when we encounter <code>ast.Raise</code> nodes:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="5">
    Here, we look for <code>raise Exception</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="6">
    or <code>raise Exception(...)</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="7">
    If either is true, we print the issue, line number, and the code itself for reference:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="8">
    Regardless of whether we found something, we make sure to continue the traversal:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="9">
    We also need to visit <code>ast.ExceptHandler</code> nodes:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="10">
    With a bare <code>except</code>, there is no exception type provided in <code>node.type</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="11">
    With a generic exception, the exception type provided is <code>Exception</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="12">
    Again, regardless of whether we found something, we continue the traversal:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="13">
    We generated the AST in <code>__init__()</code>, so we create <code>run()</code> to call <code>visit()</code>:
  </p>
</div>

<div>
<pre>
    <code data-trim class="language-python hide-line-numbers" data-line-numbers="1-2|5|6-8|10-14|11-13|16-33|18-21|22-25|27-31|33|35-44|36-38|40-42|44|46-47" data-fragment-index="0">
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
</code></pre>

---

Using the `GenericExceptionVisitor` is a little different. This time, we pass in the source code when we initialize it, and we call the `run()` method to kick off the traversal:

```pycon [highlight-lines="1-5|6-23"][class="hide-line-numbers"]
>>> source_code = Path('snippets/generic_exception.py')
>>> visitor = GenericExceptionVisitor(
...     source_code.read_text()
... )
>>> visitor.run()
Bare except on line 5:
| except:
|     pass

Generic Exception on line 11:
| except Exception:
|     pass

Generic Exception raised on line 16:
| raise Exception('Improper input format')

Generic Exception raised on line 20:
| raise Exception

Bare except on line 25:
| except:
|     print('Shame on you!')
|     raise
```

---

#### `ast.NodeTransformer`

The `ast.NodeTransformer` performs the traversal in the same way that the `ast.NodeVisitor` does, but it can modify the AST. So far, each of our `visit_*()` methods haven't returned anything (implicit return of `None`). However, with the `ast.NodeTransformer`, the return value modifies the AST:

- Returning `None` deletes the subtree rooted at that node (*i.e.*, that node and all of its descendants)
- Returning `transformed_node` replaces the subtree rooted at the visited node with `transformed_node` (or keeps it if it wasn't modified)

---

Circling back to our `try`/`except`/`pass` detector, we can create a `ast.NodeTransformer` to rewrite that code to use `contextlib.suppress()` instead of just suggesting it:

<div class="fragment semi-fade-out" data-fragment-index="0">

```python
def strip_password(x: dict[str, str]) -> None:
    try:
        del x['password']
    except KeyError:
        pass
```

</div>

<div class="fragment fade-in-then-semi-out" data-fragment-index="0">

```python
import contextlib

def strip_password(x: dict[str, str]) -> None:
    with contextlib.suppress(KeyError):
        del x['password']
```

</div>

---


<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    Once again, we will use the <code>ast</code> module along with <code>textwrap</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="0">
    We start by inheriting from <code>ast.NodeTransformer</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="1">
    Here <code>has_changed</code> indicates whether we need to add an import for <code>contextlib</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="2">
    <code>_get_suppress_block()</code> will take a <code>ast.Try</code> node and convert it:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="3">
    Rather than write the AST directly, we will write source code, parse it, then edit it:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="4">
    We <code>suppress()</code> the type of exception that was in the <code>except</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="5">
    The body of the <code>with</code> block will be the code that was in the body of the <code>try</code>:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="6">
    Finally, we return this new node so that we can update the AST:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="7">
    The <code>ast.NodeTransformer</code> will call our <code>visit_Try()</code> method during traversal:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="8">
    If it finds a <code>try</code> block to rewrite, it will report it and start the AST update:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="9">
    We track the change and call <code>_get_suppress_block()</code> to get the new node:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="10">
    We still need to traverse the tree further in case there are any nested blocks:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="11">
    By returning the new node, the <code>try</code> block is replaced by the new <code>with</code> block:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="12">
    Again, we create a <code>run()</code> method as the entrypoint:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="13">
    We start by calling <code>visit()</code> to traverse the entire AST:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="14">
    If any edits were made, we will add <code>import contextlib</code> to the top of the module:
  </p>
  <p class="fragment fade-in-then-out" data-fragment-index="15">
    We return the modified AST with all the location information required to compile:
  </p>
</div>

<div>
<pre>
    <code data-trim class="language-python hide-line-numbers" data-line-numbers="1-2|5|6-8|10-20|10-15|16-18|19|20|22-34|23-32|31-32|33|34|36-43|37|38-42|43" data-fragment-index="0">
import ast
from textwrap import dedent


class TryExceptTransformer(ast.NodeTransformer):
    def __init__(self, source_code):
        self.tree = ast.parse(source_code)
        self.has_changed = False

    def _get_suppress_block(self, node):
        suppress_example = dedent("""
        with contextlib.suppress(KeyError):
            del x['password']
        """)
        with_block = ast.parse(suppress_example).body[0]
        with_block.items[0].context_expr.args = [
            node.handlers[0].type or ast.Name('Exception')
        ]
        with_block.body = node.body
        return with_block

    def visit_Try(self, node):
        if (
            len(node.handlers) == 1
            and isinstance(node.handlers[0].body[-1], ast.Pass)
        ):
            print(
                'Detected a try/except/pass block on',
                f'line {node.lineno}, rewriting'
            )
            self.has_changed = True
            node = self._get_suppress_block(node)
        self.generic_visit(node)
        return node

    def run(self):
        result = self.visit(self.tree)
        if self.has_changed:
            self.tree.body = (
                [ast.Import([ast.alias('contextlib')])]
                + self.tree.body
            )
        return ast.fix_missing_locations(result)
</code></pre>

---


We can use the `TryExceptTransformer` on the `try_except.py` snippet to generate the modified AST. Remember that using `ast.unparse()` may result in other changes to the code, like the loss of comments and formatting:

```pycon [highlight-lines="1-3|4|5-9"][class="hide-line-numbers"]
>>> source_code = Path('snippets/try_except.py')
>>> transformer = TryExceptTransformer(source_code)
>>> updated_ast = transformer.run()
>>> print(ast.unparse(updated_ast))
import contextlib

def strip_password(x: dict[str, str]) -> None:
    with contextlib.suppress(KeyError):
        del x['password']
```

<p class="fragment"><em>Note that, in order to simplify the code, we didn't check if there was already an import of <code>contextlib</code> or even the <code>suppress()</code> function, but you could do that as well.</em><p>
