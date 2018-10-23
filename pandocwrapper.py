import subprocess
from subprocess import PIPE, STDOUT, DEVNULL
from shutil import which

"""Small pandoc wrapper.
Only TO PDF and FROM LATEX and DOCX."""

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
reference_flag: str = "--reference-doc="
datadir_flag: str = "--data-dir="
xelatex_str: str = "xelatex"
pdflatex_str: str = "pdflatex"
latex_str: str = "latex"
docx_str: str = "docx"


# BaseConverter class
class BaseConverter(object):
    """Base Converter class
    Class to convert from and to different formats, default is to convert to PDF.
    """

    def __init__(self, file_in, file_out, from_format=None, to_format=None, path_to_files=".", verbose=False):
        """
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
        :type verbose: bool, optional"""

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
        Adds argument to list of arguments, that will be executed as a command in a subprocess

        :param to_add: argument(s) to add to the argument list
        :type to_add: str or list of str
        :return: nothing
        """

        for arg in to_add:
            self.arguments.append(arg)

    def construct_command(self):
        """
        Constructs the base command, based on the class attributes.
        Always starts with `pandoc`. Second is '-f ' if given.
        Third is '-t ' if given and matching the self.file_out ending,
            otherwise changes self.file_out ending to .pdf and sets self.to_format to None.
        Last is the '--verbose' flag is self.verbose is True.

        :return: nothing
        """

        self.arguments = [pandoc_str]

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
        Converts the input file by sending the pandoc command to a subprocess.
        First adds missing, but common arguments to the arguments list:
            --pdf-engine (if self.to_format is None)
            -o self.file_out
            self.file_in
        Creates a subprocess using Popen, self.arguments is set as 'args' of the subprocess.
        Sets the working directory to self.path_to_files.
        Prints stdout and error (if happened) of subprocess to console.

        :return: nothing
        """

        if self.to_format is None:
            self.add_arguments(self.pdf_engine)
        self.add_arguments(output_flag, self.file_out, self.file_in)
        print(self)
        process = subprocess.Popen(self.arguments, stdin=PIPE, stdout=PIPE, cwd=self.path_to_files, encoding="UTF-8")
        outs, errs = process.communicate()
        print(outs)
        print("process errors: " + str(errs))


class LatexConverter(BaseConverter):
    """Latex Converter class
    Converts from latex to different formats, default is to convert to PDF."""

    def __init__(self, file_in, file_out, bib=None, template=None,
                 from_format=latex_str, to_format=None, path_to_files=".", verbose=False):
        """
        Calls BaseConverter.__init__() first.
        :param bib: Path to bibliography file (.bib), has to be placed in path_to_files.
        :param template: Path to template file (.tex), has to be placed in path_to_files.
        :type bib: str
        :type template: str
        """

        super().__init__(file_in=file_in, file_out=file_out,
                         from_format=from_format, to_format=to_format, verbose=verbose, path_to_files=path_to_files)
        self.bib = bib
        self.template = template

    def __str__(self):
        return "LatexConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        """
        Calls BaseConverter.construct_command() first.
        Adds '--bibliography=self.bib' (if self.bib is not None) to self.arguments.
        Adds '-s', '--data-dir=.' and '--template=self.template' (if self.template is not None) to self.arguments.
        '--data-dir' is set to '.' because the working directory of the subprocess will be set to self.path_to_files.

        :return: nothing
        """

        super().construct_command()
        if self.bib:
            self.add_arguments(bib_flag + self.bib)

        if self.template:
            self.add_arguments(standalone_flag)
            self.add_arguments(datadir_flag + ".")
            self.add_arguments(template_flag + self.template)


class DocxConverter(BaseConverter):
    """Docx Converter class
    Converts from docx to different formats, default is to convert to PDF."""

    def __init__(self, file_in, file_out, template=None,
                 from_format=docx_str, to_format=None, path_to_files=".", verbose=False):
        """
        Calls BaseConverter.__init__() first.
        :param template: Path to reference/template file (.docx or .tex), has to be place in path_to_files.
        :type template: str
        """

        super().__init__(file_in=file_in, file_out=file_out,
                         from_format=from_format, to_format=to_format, verbose=verbose, path_to_files=path_to_files)
        self.template = template

    def __str__(self):
        return "DocxConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        """
        Calls BaseConverter.construct_command() first.
        Adds '-s', '--data-dir=.' (if self.template is not None) to self.arguments.
        '--data-dir' is set to '.' because the working directory of the subprocess will be set to self.path_to_files.
        Adds '--template=self.template' if self.to_format is None, so output will be pdf.
        Or adds '--reference=self.template' if self.to_format is 'docx' and self.template ends in '.docx'

        :return: nothing
        """

        super().construct_command()

        if self.template:
            self.add_arguments(standalone_flag)
            self.add_arguments(datadir_flag + ".")

            if self.to_format is None:  # assuming pdf creation
                self.add_arguments(template_flag + self.template)
            elif self.to_format == docx_str and self.template.split(".")[1] == docx_str:
                self.add_arguments(reference_flag + self.template)
