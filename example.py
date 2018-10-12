import pandocwrapper


# bc = pandocwrapper.BaseConverter(file_in="files/latex.tex",
#                                 file_out="files/output.pdf",
#                                 from_format=pandocwrapper.latex_str,
#                                 verbose=True)

lc = pandocwrapper.LatexConverter(file_in="latex.tex",
                                  file_out="output.pdf",
                                  path_to_files="files/",
                                  verbose=True,
                                  template="template2.tex",
                                  bib="literatur.bib")
lc.construct_command()
lc.convert()
