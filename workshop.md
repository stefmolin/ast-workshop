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
  <img width="650" src="media/full-ast.svg" alt="The AST for greet.py visualized with Graphviz" data-preview-image>
  <br/>
  <small>The AST for <code>greet.py</code> visualized with Graphviz.</small>
</div>

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

[id=exercise-1-1]
## Exercise

Try passing source code that has a `SyntaxError` into `ast.parse()`. What happens? What about if the code has a non-syntax error?

---

[id=example-solution-1-1]
## Example solution

<div class="fragment">

### Syntactically-incorrect source code

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

### Syntactically-correct source code with logic errors

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

[id=inspecting-the-ast]
### Inspecting the AST

<div class="r-stack r-stack-left">
  <p class="fragment fade-out" data-fragment-index="0">
    Use <code>ast.dump()</code> to display the AST:
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

[id=exercise-1-2]
## Exercise

The AST is a abstract representation of the source code's logic created by the parser as an intermediary step when [compiling source code into byte code](https://github.com/python/cpython/blob/main/InternalDocs/compiler.md) (necessary to run it). Non-code elements like comments and formatting don't make it to the AST, so while we can use `ast.unparse()` to convert an AST into source code, it will not identical to the starting code. Create a code snippet with comments and custom formatting/styling and try to round-trip it. What differences do you notice?

```pycon [highlight-lines="4"][class="hide-line-numbers"]
>>> import ast
>>> source_code = 'TODO'
>>> tree = ast.parse(source_code)
>>> print(ast.unparse(tree))
```

---

[id=example-solution-1-2]
## Example solution

Consider the following source code (stored as a string in a variable called `source_code`):

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

When we parse this into an AST and back to source code, several things have changed:

```pycon [highlight-lines="1-3|4-12"][class="hide-line-numbers"]
>>> import ast
>>> tree = ast.parse(source_code)
>>> print(ast.unparse(tree))
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
