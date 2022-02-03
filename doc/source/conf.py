# noqa: E265
#
# khal documentation build configuration file, created by
# sphinx-quickstart on Fri Jul  4 00:00:47 2014.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import validate
from configobj import ConfigObj

import khal

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- Generate configspec.rst ----------------------------------------------

specpath = '../../khal/settings/khal.spec'
config = ConfigObj(
    None, configspec=specpath, stringify=False, list_values=False
)
validator = validate.Validator()
config.validate(validator)
spec = config.configspec


def write_section(specsection, secname, key, comment, output):
    # why is _parse_check a "private" method? seems to be rather useful...
    # we don't need fun_kwargs
    fun_name, fun_args, fun_kwargs, default = validator._parse_check(specsection)
    output.write(f'\n.. _{secname}-{key}:')
    output.write('\n')
    output.write(f'\n.. object:: {key}\n')
    output.write('\n')
    output.write('    ' + '\n    '.join([line.strip('# ') for line in comment]))
    output.write('\n')
    if fun_name == 'option':
        fun_args = [f'*{arg}*' for arg in fun_args]
        fun_args = fun_args[:-2] + [fun_args[-2] + ' and ' + fun_args[-1]]
        fun_name += f", allowed values are {', '.join(fun_args)}"
        fun_args = []
    if fun_name == 'integer' and len(fun_args) == 2:
        fun_name += f', allowed values are between {fun_args[0]} and {fun_args[1]}'
        fun_args = []
    output.write('\n')
    if fun_name in ['expand_db_path', 'expand_path']:
        fun_name = 'string'
    elif fun_name in ['force_list']:
        fun_name = 'list'
        if isinstance(default, list):
            default = ['space' if one == ' ' else one for one in default]
            default = ', '.join(default)

    output.write(f'      :type: {fun_name}')
    output.write('\n')
    if fun_args != []:
        output.write(f'      :args: {fun_args}')
        output.write('\n')
    output.write(f'      :default: {default}')
    output.write('\n')


with open('configspec.rst', 'w') as f:
    for secname in sorted(spec):
        f.write('\n')
        heading = f'The [{secname}] section'
        f.write(f'{heading}\n{ len(heading) * "~"}')
        f.write('\n')
        comment = spec.comments[secname]
        f.write('\n'.join([line[2:] for line in comment]))
        f.write('\n')

        for key, comment in sorted(spec[secname].comments.items()):
            if key == '__many__':
                comment = spec[secname].comments[key]
                f.write('\n'.join([line[2:] for line in comment]))
                f.write('\n')
                for key, comment in sorted(spec[secname]['__many__'].comments.items()):
                    write_section(spec[secname]['__many__'][key], secname,
                                  key, comment, f)
            else:
                write_section(spec[secname][key], secname, key, comment, f)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinxcontrib.newsfeed',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['ytemplates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'khal'
copyright = 'Copyright (c) 2013-2021 khal contributors'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = khal.__version__
# The full version, including alpha/beta/rc tags.
release = khal.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['configspec.rst']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'github_user': 'pimutils',
    'github_repo': 'khal',
}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['ystatic']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'khaldoc'

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('man', 'khal', 'khal Documentation',
     ['Christan Geier et al.'], 1)
]

# If true, show URL addresses after external links.
man_show_urls = True


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'khal', 'khal Documentation',
     'khal contributors', 'khal', 'A standards based calendar program',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}
