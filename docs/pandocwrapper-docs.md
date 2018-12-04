::: {.related role="navigation" aria-label="related navigation"}
### Navigation

-   [index](../genindex.html "General Index")
-   [modules](../py-modindex.html "Python Module Index") \|
-   [pandocwrapper documentation](../index.html) »
:::

::: {.document}
::: {.documentwrapper}
::: {.bodywrapper}
::: {.body role="main"}
::: {#module-pandocwrapper .section}
[]{#pandocwrapper-module}

pandocwrapper module[¶](#module-pandocwrapper "Permalink to this headline"){.headerlink}
========================================================================================

 *class* `pandocwrapper.`{.descclassname}`BaseConverter`{.descname}[(]{.sig-paren}*file\_in*, *file\_out=None*, *from\_format=None*, *to\_format=None*, *path\_to\_files=\'.\'*, *verbose=False*[)]{.sig-paren}[¶](#pandocwrapper.BaseConverter "Permalink to this definition"){.headerlink}

:   Bases: [`object`{.xref .py .py-class .docutils .literal
    .notranslate}](https://docs.python.org/3/library/functions.html#object "(in Python v3.7)"){.reference
    .external}

    Base Converter

    Class to convert from and to different formats, default is to
    convert to PDF.

     `add_arguments`{.descname}[(]{.sig-paren}*\*to\_add*[)]{.sig-paren}[¶](#pandocwrapper.BaseConverter.add_arguments "Permalink to this definition"){.headerlink}

    :   Adds argument to list of arguments(`self.arguments`{.code
        .docutils .literal .notranslate}), that will be executed as a
        command in a subprocess

          ------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          Parameters:   **to\_add** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.7)"){.reference .external} *or* *list of str*) \-- argument(s) to add to the argument list
          Returns:      nothing
          ------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

     `construct_command`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#pandocwrapper.BaseConverter.construct_command "Permalink to this definition"){.headerlink}

    :   Constructs the base command, based on the class attributes.

        Always starts with `pandoc`{.code .docutils .literal
        .notranslate}. Second is `-f`{.code .docutils .literal
        .notranslate} if `self.from_format`{.code .docutils .literal
        .notranslate} given. Third is `-t`{.code .docutils .literal
        .notranslate} if given and matching the `self.file_out`{.code
        .docutils .literal .notranslate} ending, otherwise changes
        `self.file_out`{.code .docutils .literal .notranslate} ending to
        .pdf and sets `self.to_format`{.code .docutils .literal
        .notranslate} to `None`{.code .docutils .literal .notranslate}.
        Last is the `--verbose`{.code .docutils .literal .notranslate}
        flag if `self.verbose`{.code .docutils .literal .notranslate} is
        `True`{.code .docutils .literal .notranslate}.

          ---------- ---------
          Returns:   nothing
          ---------- ---------

     `convert`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#pandocwrapper.BaseConverter.convert "Permalink to this definition"){.headerlink}

    :   Converts the input file by sending the pandoc command to a
        subprocess.

        First adds missing, but common arguments to the arguments list:

        :   `--pdf-engine`{.code .docutils .literal .notranslate} (if
            `self.to_format`{.code .docutils .literal .notranslate} is
            `None`{.code .docutils .literal .notranslate})

            `-o self.file_out`{.code .docutils .literal .notranslate}

            `self.file_in`{.code .docutils .literal .notranslate}

        Creates a subprocess using
        [Popen](https://docs.python.org/2/library/subprocess.html#subprocess.Popen){.reference
        .external}, `self.arguments`{.code .docutils .literal
        .notranslate} is set as `args`{.code .docutils .literal
        .notranslate} of the subprocess. Sets the working directory
        (`cwd`{.code .docutils .literal .notranslate}) to
        `self.path_to_files`{.code .docutils .literal .notranslate}.

        Prints stdout and error (if happened) of subprocess to console.

          ---------- ---------
          Returns:   nothing
          ---------- ---------

<!-- -->

 *class* `pandocwrapper.`{.descclassname}`DocxConverter`{.descname}[(]{.sig-paren}*file\_in*, *file\_out=None*, *template=None*, *from\_format=\'docx\'*, *to\_format=None*, *path\_to\_files=\'.\'*, *verbose=False*[)]{.sig-paren}[¶](#pandocwrapper.DocxConverter "Permalink to this definition"){.headerlink}

:   Bases: [`pandocwrapper.BaseConverter`{.xref .py .py-class .docutils
    .literal
    .notranslate}](#pandocwrapper.BaseConverter "pandocwrapper.BaseConverter"){.reference
    .internal}

    Docx Converter

    Converts from docx to different formats, default is to convert to
    PDF.

     `construct_command`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#pandocwrapper.DocxConverter.construct_command "Permalink to this definition"){.headerlink}

    :   Calls `BaseConverter.construct_command()`{.code .docutils
        .literal .notranslate} first.

        Sets `self.template`{.code .docutils .literal .notranslate} to
        htwberlin.tex, if `self.template`{.code .docutils .literal
        .notranslate} is not None. Adds `-s`{.code .docutils .literal
        .notranslate}, `--data-dir=.`{.code .docutils .literal
        .notranslate} to `self.arguments`{.code .docutils .literal
        .notranslate}. `--data-dir`{.code .docutils .literal
        .notranslate} is set to the current directory because the
        working directory of the subprocess will be set to
        `self.path_to_files`{.code .docutils .literal .notranslate}.
        Adds `--template=self.template`{.code .docutils .literal
        .notranslate} if `self.to_format`{.code .docutils .literal
        .notranslate} is None, so output will be pdf. Or adds
        `--reference=self.template`{.code .docutils .literal
        .notranslate} if `self.to_format`{.code .docutils .literal
        .notranslate} is docx and `self.template`{.code .docutils
        .literal .notranslate} ends in .docx

          ---------- ---------
          Returns:   nothing
          ---------- ---------

<!-- -->

 *class* `pandocwrapper.`{.descclassname}`LatexConverter`{.descname}[(]{.sig-paren}*file\_in*, *file\_out=None*, *bib=None*, *template=None*, *resources\_path=None*, *from\_format=\'latex\'*, *to\_format=None*, *path\_to\_files=\'.\'*, *verbose=False*[)]{.sig-paren}[¶](#pandocwrapper.LatexConverter "Permalink to this definition"){.headerlink}

:   Bases: [`pandocwrapper.BaseConverter`{.xref .py .py-class .docutils
    .literal
    .notranslate}](#pandocwrapper.BaseConverter "pandocwrapper.BaseConverter"){.reference
    .internal}

    Latex Converter

    Converts from latex to different formats, default is to convert to
    PDF.

     `construct_command`{.descname}[(]{.sig-paren}[)]{.sig-paren}[¶](#pandocwrapper.LatexConverter.construct_command "Permalink to this definition"){.headerlink}

    :   Calls `BaseConverter.construct_command()`{.code .docutils
        .literal .notranslate} first.

        Sets `self.template`{.code .docutils .literal .notranslate} to
        htwberlin.tex, if `self.template`{.code .docutils .literal
        .notranslate} is not None. Adds `--bibliography=self.bib`{.code
        .docutils .literal .notranslate} (if `self.bib`{.code .docutils
        .literal .notranslate} is not `None`{.code .docutils .literal
        .notranslate}) to `self.arguments`{.code .docutils .literal
        .notranslate}. Adds `-s`{.code .docutils .literal .notranslate},
        `--data-dir=.`{.code .docutils .literal .notranslate} and
        `--template=self.template`{.code .docutils .literal
        .notranslate} to `self.arguments`{.code .docutils .literal
        .notranslate}. `--data-dir`{.code .docutils .literal
        .notranslate} is set to the current directory because the
        working directory of the subprocess will be set to
        `self.path_to_files`{.code .docutils .literal .notranslate}.

          ---------- ---------
          Returns:   nothing
          ---------- ---------
:::
:::
:::
:::

::: {.sphinxsidebar role="navigation" aria-label="main navigation"}
::: {.sphinxsidebarwrapper}
::: {role="note" aria-label="source link"}
### This Page

-   [Show Source](../_sources/source/pandocwrapper.rst.txt)
:::

::: {#searchbox style="display: none" role="search"}
### Quick search

::: {.searchformwrapper}
:::
:::
:::
:::

::: {.clearer}
:::
:::

::: {.related role="navigation" aria-label="related navigation"}
### Navigation

-   [index](../genindex.html "General Index")
-   [modules](../py-modindex.html "Python Module Index") \|
-   [pandocwrapper documentation](../index.html) »
:::

::: {.footer role="contentinfo"}
© Copyright 2018, Jakob Pfeiffer. Created using
[Sphinx](http://sphinx-doc.org/) 1.8.1.
:::
