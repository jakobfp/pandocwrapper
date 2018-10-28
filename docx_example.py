import pandocwrapper

# create docx converter
dc = pandocwrapper.DocxConverter(file_in="examples/docx/docx_example.docx",
                                 path_to_files="cis/latex/",
                                 template="htwberlin.tex",
                                 verbose=True)
dc.construct_command()  # construct the command
dc.convert()  # convert to desired format
