import pandocwrapper


lc = pandocwrapper.LatexConverter(file_in="latex.tex",
                                  file_out="output.pdf",
                                  path_to_files="files/",
                                  verbose=True,
                                  template="template2.tex",
                                  bib="literatur.bib")
lc.construct_command()
lc.convert()
