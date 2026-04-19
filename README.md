# Process, Analyze, and Transform Python Code with ASTs

[![View slides in browser](https://img.shields.io/badge/view-slides-orange?logo=reveal.js&logoColor=white)](https://stefaniemolin.com/ast-workshop/) [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

The [slides](https://stefaniemolin.com/ast-workshop/) are licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa]. Any code files in this repository are distributed under the Apache-2.0 license.

See [my website](https://stefaniemolin.com/workshops/ast-workshop/) for additional information about this workshop.

## Abstract

You’ve likely used a tool like `black`, `flake8`, or `ruff` to lint or format your code, or a tool like `sphinx` to document it, but you probably do not know how they accomplish their tasks. These tools and many more use **Abstract Syntax Trees (ASTs)** to analyze and extract information from Python code. An AST is a representation of your code's structure that enables you to access and manipulate its different components, which is what makes it possible to automate tasks like code migrations, linting, and docstring extraction.

In this workshop, you’ll learn how to use the Python standard library’s `ast` module to parse and analyze code. Using just the standard library, we will implement a couple of common checks from scratch, which will give you an idea of how these tools work and help you build the skills and confidence to use ASTs in your own projects.

## Setup Instructions

1. Fork and clone this repository: [github.com/stefmolin/ast-workshop](https://github.com/stefmolin/ast-workshop/). If you don't have a GitHub account, you will need to create one to complete this step. Please be sure to check for changes (and sync them) before coming to the workshop.

2. Confirm that you have Python 3.10 or higher installed (3.14 is preferred), as well as a text editor for writing code.

3. Open up these slides in your browser and use the arrow keys to follow along: [stefaniemolin.com/ast-workshop](https://stefaniemolin.com/ast-workshop/).

4. Open up the documentation for the `ast` module in your browser to consult during the exercises: [docs.python.org/3/library/ast.html](https://docs.python.org/3/library/ast.html).

## About the Author

[![Github Sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&link=https://github.com/sponsors/stefmolin&style=flat)](https://github.com/sponsors/stefmolin)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-yellow?style=flat&logo=buymeacoffee&logoColor=white&labelColor=yellow&color=gray)](https://www.buymeacoffee.com/stefanie.molin)
[![Ko-Fi](https://shields.io/badge/kofi-Support-ff5f5f?logo=ko-fi&style=flat)](https://ko-fi.com/stefaniemolin)

[Stefanie Molin](https://stefaniemolin.com/) ([@stefmolin](https://github.com/stefmolin)) is a software engineer and data scientist at Bloomberg in New York City, where she tackles tough problems in information security, particularly those revolving around data wrangling/visualization, building tools for gathering data, and knowledge sharing. She is also the author of *[Hands-On Data Analysis with Pandas](https://www.amazon.com/dp/1800563450/)*, which is currently in its second edition and has been translated into Korean and Chinese. She holds a bachelor’s of science degree in operations research from Columbia University's Fu Foundation School of Engineering and Applied Science, as well as a master’s degree in computer science, with a specialization in machine learning, from Georgia Tech. In her free time, she enjoys traveling the world, inventing new recipes, and learning new languages spoken among both people and computers.

## Help support this project

Since March 2026, I have dedicated **80+ hours of my personal time** to creating and maintaining this free and open-source workshop. If you can, please consider helping support this project by [sponsoring me on GitHub](https://github.com/sponsors/stefmolin), [buying me a coffee](https://www.buymeacoffee.com/stefanie.molin), or [supporting me on Ko-Fi](https://ko-fi.com/stefaniemolin).

## Licenses

### Code
Any code files in this repository are distributed under the Apache-2.0 license.

### Slides
The slides are licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
