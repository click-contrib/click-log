# -*- coding: utf-8 -*-

import sys
import os

import click_log

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'

project = 'click-log'
copyright = '2016, Markus Unterwaditzer & contributors'
author = 'Markus Unterwaditzer & contributors'

release = click_log.__version__
version = '.'.join(release.split('.')[:2])  # The short X.Y version.

exclude_patterns = ['_build']

pygments_style = 'sphinx'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

try:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
except ImportError:
    html_theme = 'default'
    if not on_rtd:
        print('-' * 74)
        print('Warning: sphinx-rtd-theme not installed, building with default '
              'theme.')
        print('-' * 74)

html_static_path = ['_static']
htmlhelp_basename = 'click-logdoc'

latex_elements = {}

latex_documents = [
    (master_doc, 'click-log.tex', 'click-log Documentation',
     'Markus Unterwaditzer \\& contributors', 'manual'),
]

man_pages = [
    (master_doc, 'click-log', 'click-log Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'click-log', 'click-log Documentation',
     author, 'click-log', 'One line description of project.',
     'Miscellaneous'),
]
