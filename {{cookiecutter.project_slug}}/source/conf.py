"""Sphinx configuration for {{ cookiecutter.project_name }}."""

from pathlib import Path


project = {{ cookiecutter.project_name | tojson }}
author = {{ cookiecutter.author_name | tojson }}
copyright = {{ (cookiecutter.copyright_year ~ ", " ~ cookiecutter.author_name) | tojson }}
release = {{ cookiecutter.semester | tojson }}

extensions = [
    "sphinx.ext.autosectionlabel",
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinxemoji.sphinxemoji",
]

autosectionlabel_prefix_document = True
source_suffix = {".md": "markdown"}
root_doc = "index"
language = "{{ cookiecutter.language }}"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3

html_theme = "shibuya"
html_title = {{ cookiecutter.project_name | tojson }}
html_baseurl = {{ cookiecutter.site_url | tojson }}
html_theme_options = {
    "accent_color": "tomato",
    "color_mode": "auto",
    # Two levels work better for chapter/section style course navigation while
    # keeping deeply nested lecture headings collapsed by default.
    "globaltoc_expand_depth": 2,
    "toctree_maxdepth": 3,
    "show_ai_links": False,
}
html_static_path = ["_static"]
html_css_files = [
    "https://cdn.jsdelivr.net/npm/source-sans@3.52.0/source-sans-3VF.css",
    "css/site.css",
]
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

{% if cookiecutter.include_pdf == "yes" -%}
latex_engine = "xelatex"
latex_show_urls = "footnote"
latex_documents = [
    ("index", "{{ cookiecutter.project_slug }}.tex", {{ cookiecutter.project_name | tojson }}, {{ cookiecutter.author_name | tojson }}, "manual"),
]
latex_elements = {
    "preamble": r"""
{% if cookiecutter.language == "zh_CN" -%}
\usepackage{xeCJK}
{% endif -%}
\usepackage{hyperref}
\usepackage{url}
\raggedbottom
\setlength{\parskip}{5pt}
""",
}
{% endif -%}

# Fail early if brand assets are accidentally removed.
for asset in ("logo.svg", "favicon.svg"):
    if not (Path(__file__).parent / "_static" / asset).is_file():
        raise FileNotFoundError(f"Missing brand asset: {asset}")
