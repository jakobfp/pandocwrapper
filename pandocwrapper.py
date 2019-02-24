import subprocess
from subprocess import PIPE, STDOUT, DEVNULL
from shutil import which

"""Small pandoc wrapper.

Only TO PDF and FROM LATEX, DOCX and ODT.
"""

# CONSTS
pandoc_str: str = which('pandoc')
output_flag: str = "-o"
from_flag: str = "-f"
to_flag: str = "-t"
pdf_engine_flag: str = "--pdf-engine="
verbose_flag: str = "--verbose"
standalone_flag: str = "--standalone"
bib_flag: str = "--bibliography="
template_flag: str = "--template="
resources_flag: str = "--resource-path="
reference_flag: str = "--reference-doc="
datadir_flag: str = "--data-dir="
toc_flag: str = "--toc"
beamer_str: str = "beamer"
xelatex_str: str = "xelatex"
pdflatex_str: str = "pdflatex"
latex_str: str = "latex"
docx_str: str = "docx"
odt_str: str = "odt"
markdown_str: str = "markdown"

# TEMPLATES
htw_template_str: str = "htwberlin.tex"
htw_beamer_template_str: str = "htwberlin-beamer.tex"


# BaseConverter class
class BaseConverter(object):
    """Base Converter

    Class to convert from and to different formats, default is to convert to PDF.
    """

    def __init__(self, file_in, file_out=None, from_format=None, to_format=None, path_to_files=".", verbose=False):
        """
        function:: __init__(self, file_in, file_out, from_format=None, to_format=None, path_to_files=".", verbose=False)

        Constructor

        :param file_in: Path to file to be converted
        :param file_out: Path to output file
        :param from_format: Format of input file (default is None), pandoc will determine if None
        :param to_format: Format to which will be converted (default is None), will be converted to PDF if None
        :param path_to_files: Path to template/reference files (default is '.')
        :param verbose: Set verbose output of pandoc (default is False)
        :type file_in: str
        :type file_out: str
        :type from_format: str, optional
        :type to_format: str, optional
        :type path_to_files: str, optional
        :type verbose: bool, optional
        """

        self.from_format = from_format
        self.to_format = to_format
        self.file_in = file_in
        self.file_out = file_out
        self.pdf_engine = pdf_engine_flag + xelatex_str
        self.verbose = verbose
        self.path_to_files = path_to_files
        self.arguments = []

    def __str__(self):
        return "BaseConverter(" + str(self.arguments) + ")"

    def add_arguments(self, *to_add):
        """
        Adds argument to list of arguments(:code:`self.arguments`), that will be executed as a command in a subprocess


        :param to_add: argument(s) to add to the argument list
        :type to_add: str or list of str
        :returns: nothing
        """

        for arg in to_add:
            self.arguments.append(arg)

    def construct_command(self):
        """
        Constructs the base command, based on the class attributes.

        Always starts with :code:`pandoc`. Second is :code:`-f` if :code:`self.from_format` given.
        Third is :code:`-t` if given and matching the :code:`self.file_out` ending,
        otherwise changes :code:`self.file_out` ending to `.pdf` and sets :code:`self.to_format` to :code:`None`.
        Last is the :code:`--verbose` flag if :code:`self.verbose` is :code:`True`.


        :returns: nothing
        """

        self.arguments = [pandoc_str]

        if not self.file_out:
            self.file_out = str(self.file_in.split('.')[0] + "-output.pdf")

        if self.from_format:
            self.add_arguments(from_flag, self.from_format)

        if self.to_format:
            if self.file_out.split(".")[1] == self.to_format:
                self.add_arguments(to_flag, self.to_format)
            else:
                print("not matching format ("
                      + self.file_out.split(".")[1]
                      + " != "
                      + self.to_format
                      + ") - will try pdf...")
                self.to_format = None
                self.file_out = self.file_out.split(".")[0] + ".pdf"

        if self.verbose:
            self.add_arguments(verbose_flag)

    def convert(self):
        """
        Converts the input file by sending the `pandoc` command to a subprocess.

        First adds missing, but common arguments to the arguments list:
            :code:`--pdf-engine` (if :code:`self.to_format` is :code:`None`)

            :code:`-o self.file_out`

            :code:`self.file_in`

        Creates a subprocess using `Popen`_, :code:`self.arguments` is set as :code:`args` of the subprocess.
        Sets the working directory (:code:`cwd`) to :code:`self.path_to_files`.

        .. _Popen: https://docs.python.org/2/library/subprocess.html#subprocess.Popen

        Prints `stdout` and `error` (if happened) of subprocess to console.

        :returns: nothing
        """

        if self.to_format is None or self.to_format is beamer_str:
            self.add_arguments(self.pdf_engine)
        self.add_arguments(output_flag, self.file_out, self.file_in)
        print(self)
        process = subprocess.Popen(self.arguments, stdin=PIPE, stdout=PIPE, cwd=self.path_to_files, encoding="UTF-8")
        outs, errs = process.communicate()
        print(outs)
        print("process errors: " + str(errs))
        return errs


class LatexConverter(BaseConverter):
    """Latex Converter

    Converts from latex to different formats, default is to convert to PDF."""

    def __init__(self, file_in, file_out=None, bib=None, template=None, resources_path=None,
                 from_format=latex_str, to_format=None, path_to_files=".", verbose=False):
        """
        Calls :code:`BaseConverter.__init__()` first.


        :param bib: Path to bibliography file (.bib), has to be placed in path_to_files.
        :param template: Path to template file (.tex), has to be placed in path_to_files.
        :param resources_path: Path to resource (images etc.) files (default is '.')
        :type bib: str
        :type template: str
        :type resources_path: str, optional (default is None, will be set to path of :code:`self.file_in`)
        """

        super().__init__(file_in=file_in, file_out=file_out,
                         from_format=from_format, to_format=to_format, verbose=verbose,
                         path_to_files=path_to_files)
        self.bib = bib
        self.template = template
        self.resources_path = resources_path

    def __str__(self):
        return "LatexConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        """
        Calls :code:`BaseConverter.construct_command()` first.

        Sets :code:`self.template` to `htwberlin.tex`, if :code:`self.template` is not None.
        Adds :code:`--bibliography=self.bib` (if :code:`self.bib` is not :code:`None`) to :code:`self.arguments`.
        Adds :code:`-s`, :code:`--data-dir=.` and :code:`--template=self.template` to :code:`self.arguments`.
        :code:`--data-dir` is set to the current directory because the working directory of the subprocess
        will be set to :code:`self.path_to_files`.


        :returns: nothing
        """

        super().construct_command()

        if not self.resources_path:
            self.resources_path = "/".join(self.file_in.split("/")[:-1])

        if not self.template:
            print("not template given - using htwberlin.tex...")
            self.template = htw_template_str

        if self.bib:
            self.add_arguments(bib_flag + self.bib)

        self.add_arguments(standalone_flag)
        self.add_arguments(datadir_flag + ".")
        self.add_arguments(template_flag + self.template)
        self.add_arguments(resources_flag + self.resources_path)


class DocxConverter(BaseConverter):
    """Docx Converter

    Converts from docx to different formats, default is to convert to PDF."""

    def __init__(self, file_in, file_out=None, template=None,
                 from_format=docx_str, to_format=None, path_to_files=".", verbose=False):
        """
        Calls :code:`BaseConverter.__init__()` first.

        :param template: Path to reference/template file (.docx or .tex), has to be placed in path_to_files.
        :type template: str
        """

        super().__init__(file_in=file_in, file_out=file_out,
                         from_format=from_format, to_format=to_format, verbose=verbose,
                         path_to_files=path_to_files)
        self.template = template

    def __str__(self):
        return "DocxConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        """
        Calls :code:`BaseConverter.construct_command()` first.

        Sets :code:`self.template` to `htwberlin.tex`, if :code:`self.template` is not None.
        Adds :code:`-s`, :code:`--data-dir=.` to :code:`self.arguments`.
        :code:`--data-dir` is set to the current directory because the working directory of the subprocess
        will be set to :code:`self.path_to_files`.
        Adds :code:`--template=self.template` if :code:`self.to_format` is None, so output will be pdf.
        Or adds :code:`--reference=self.template` if :code:`self.to_format` is `docx` and :code:`self.template` ends in `.docx`


        :returns: nothing
        """

        super().construct_command()

        if not self.template:
            print("not template given - using htwberlin.tex...")
            self.template = htw_template_str

        self.add_arguments(standalone_flag)
        self.add_arguments(datadir_flag + ".")

        if self.to_format is None:  # assuming pdf creation
            self.add_arguments(template_flag + self.template)
        elif self.to_format == docx_str and self.template.split(".")[1] == docx_str:
            self.add_arguments(reference_flag + self.template)


class OdtConverter(BaseConverter):
    """Odt Converter

    Converts from odt to different formats, default is to convert to PDF."""

    def __init__(self, file_in, file_out=None, template=None,
                 from_format=odt_str, to_format=None, path_to_files=".", verbose=False):
        """
        Calls :code:`BaseConverter.__init__()` first.

        :param template: Path to reference/template file (.odt or .tex), has to be placed in path_to_files.
        :type template: str
        """

        super().__init__(file_in=file_in, file_out=file_out,
                         from_format=from_format, to_format=to_format, verbose=verbose,
                         path_to_files=path_to_files)
        self.template = template

    def __str__(self):
        return "OdtConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        """
        Calls :code:`BaseConverter.construct_command()` first.

        Sets :code:`self.template` to `htwberlin.tex`, if :code:`self.template` is not None.
        Adds :code:`-s`, :code:`--data-dir=.` to :code:`self.arguments`.
        :code:`--data-dir` is set to the current directory because the working directory of the subprocess
        will be set to :code:`self.path_to_files`.
        Adds :code:`--template=self.template` if :code:`self.to_format` is None, so output will be pdf.
        Or adds :code:`--reference=self.template` if :code:`self.to_format` is `odt` and :code:`self.template` ends in `.odt`


        :returns: nothing
        """

        super().construct_command()

        if not self.template:
            print("not template given - using htwberlin.tex...")
            self.template = htw_template_str

        self.add_arguments(standalone_flag)
        self.add_arguments(datadir_flag + ".")

        if self.to_format is None:  # assuming pdf creation
            self.add_arguments(template_flag + self.template)
        elif self.to_format == odt_str and self.template.split(".")[1] == odt_str:
            self.add_arguments(reference_flag + self.template)


class MdConverter(BaseConverter):
    """Markdown Converter

    Converts from markdown to PDF using beamer"""

    def __init__(self, file_in, file_out=None, template=None,
                 from_format=markdown_str, path_to_files=".", verbose=False, toc=False):
        """
        Calls :code:`BaseConverter.__init__()` first.

        :param template: Path to template file (.tex), has to be placed in path_to_files.
        :type template: str
        """

        super().__init__(file_in=file_in, file_out=file_out,
                         from_format=from_format, to_format=None, verbose=verbose,
                         path_to_files=path_to_files)
        self.template = template
        self.toc = toc

    def __str__(self):
        return "MdConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        """
        Calls :code:`BaseConverter.construct_command()` first.

        Sets :code:`self.template` to `htwberlin-beamer.tex`, if :code:`self.template` is not None.
        Adds :code:`-s`, :code:`--data-dir=.` to :code:`self.arguments`.
        :code:`--data-dir` is set to the current directory because the working directory of the subprocess
        will be set to :code:`self.path_to_files`.
        Adds `-t beamer`!


        :returns: nothing
        """

        super().construct_command()

        if not self.template:
            print("not template given - using htwberlin-beamer.tex...")
            self.template = htw_beamer_template_str

        if self.toc:
            self.add_arguments(toc_flag)

        self.add_arguments(standalone_flag)
        self.add_arguments(datadir_flag + ".")
        self.add_arguments(to_flag, beamer_str)
        self.add_arguments(template_flag + self.template)
