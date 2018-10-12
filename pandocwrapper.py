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

    def __str__(self):
        return "in: " + str(self.file_in) + \
               " out: " + str(self.file_out) + \
               " engine: " + str(self.pdf_engine) + \
               " verbose: " + str(self.verbose)

    def convert(self):

        arguments = [pandoc_str]
        if self.from_format:
            arguments.append(from_flag)
            arguments.append(self.from_format)

        if self.verbose:
            arguments.append(verbose_flag)

        arguments.append(self.pdf_engine)
        arguments.append(output_flag)
        arguments.append(self.file_out)
        arguments.append(self.file_in)

        print(arguments)

        process = subprocess.Popen(arguments, stdin=PIPE, stdout=PIPE)
        outs, errs = process.communicate()

        print(outs)
        print(errs)

