import subprocess
from subprocess import PIPE, STDOUT, DEVNULL
from shutil import which
import shlex

"""Small pandoc wrapper.
Only TO PDF and FROM LATEX and DOCX."""


# CONSTS
pandoc_str: str = which('pandoc')
output_flag: str = "-o"
from_flag: str = "-f"
pdf_engine_flag: str = "--pdf-engine="
verbose_flag: str = "--verbose"
bib_flag: str = "--bibliography="
template_flag: str = "--template="
datadir_flag: str = "--data-dir="
xelatex_str: str = "xelatex"
pdflatex_str: str = "pdflatex"
latex_str: str = "latex"
docx_str: str = "docx"


# BaseConverter class
class BaseConverter(object):
    """Base Converter class

    """

    def __init__(self, file_in, file_out, from_format=None, path_to_files=".", verbose=False):
        self.from_format = from_format
        self.file_in = file_in
        self.file_out = file_out
        self.pdf_engine = pdf_engine_flag + xelatex_str
        self.verbose = verbose
        self.path_to_files = path_to_files
        self.arguments = []

    def __str__(self):
        return "BaseConverter(" + str(self.arguments) + ")"

    def add_arguments(self, *to_add):
        for arg in to_add:
            self.arguments.append(arg)

    def construct_command(self):
        self.arguments = [pandoc_str]

        if self.from_format:
            self.add_arguments(from_flag, self.from_format)

        if self.verbose:
            self.add_arguments(verbose_flag)

    def convert(self):
        # add last important args only before executing
        self.add_arguments(self.pdf_engine, output_flag, self.file_out, self.file_in)
        print(self)
        process = subprocess.Popen(self.arguments, stdin=PIPE, stdout=PIPE, cwd=self.path_to_files, encoding="UTF-8")
        outs, errs = process.communicate()
        print(outs)
        print("process errors: " + str(errs))


class LatexConverter(BaseConverter):

    def __init__(self, file_in, file_out, bib=None, template=None, from_format=latex_str, path_to_files=".", verbose=False):
        super().__init__(file_in, file_out, from_format, path_to_files, verbose)
        self.bib = bib
        self.template = template

    def __str__(self):
        return "LatexConverter(" + str(self.arguments) + ")"

    def construct_command(self):
        super().construct_command()
        if self.bib:
            self.add_arguments(bib_flag + self.bib)

        if self.template:
            self.add_arguments(datadir_flag + ".")
            self.add_arguments(template_flag + self.template)

