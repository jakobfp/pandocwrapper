import pandocwrapper


lc = pandocwrapper.LatexConverter(file_in="examples/latex/latex_example.tex",
                                  path_to_files="cis/latex",
                                  verbose=True,
                                  template="htwberlin.tex",
                                  bib="examples/latex/literatur.bib")
lc.construct_command()
lc.convert()
