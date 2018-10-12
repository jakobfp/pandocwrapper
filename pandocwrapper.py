import subprocess
from subprocess import PIPE, STDOUT, DEVNULL
import shlex

"""Small pandoc wrapper.
Only TO PDF and FROM LATEX and DOCX."""

try:
    from shutil import which
except ImportError:
    from distutils.spawn import find_executable

    which = find_executable

# CONSTS
pandoc_str: str = which('pandoc')
output_flag: str = "-o"
from_flag: str = "-f"
pdf_engine_flag: str = "--pdf-engine="
verbose_flag: str = "--verbose"
xelatex_str: str = "xelatex"
pdflatex_str: str = "pdflatex"
latex_str: str = "latex"
docx_str: str = "docx"


# BaseConverter class
class BaseConverter(object):
    """Base Converter class

    """

    def __init__(self, file_in, file_out, from_format=None, verbose=False):
        self.from_format = from_format
        self.file_in = file_in
        self.file_out = file_out
        self.pdf_engine = pdf_engine_flag + xelatex_str
        self.verbose = verbose

        self.arguments = [pandoc_str]
        if self.from_format:
            self.add_arguments(from_flag, self.from_format)

        if self.verbose:
            self.add_arguments(verbose_flag)

        self.add_arguments(self.pdf_engine, output_flag, self.file_out, self.file_in)

    def __str__(self):
        return "Converter("+str(self.arguments)+")"

    def add_arguments(self, *to_add):
        for arg in to_add:
            self.arguments.append(arg)

    def convert(self):

        print(self)

        process = subprocess.Popen(self.arguments, stdin=PIPE, stdout=PIPE, encoding="UTF-8")
        outs, errs = process.communicate()

        print(outs)
        print("errors:" + errs)
