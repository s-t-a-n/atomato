"""Sphinx configuration."""
project = "Atomato"
author = "s-t-a-n"
copyright = "2023, s-t-a-n"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
