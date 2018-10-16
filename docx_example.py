import pandocwrapper

dc = pandocwrapper.DocxConverter(file_in="example30.docx",
                                 file_out="htw30.docx",
                                 path_to_files="files/",
                                 to_format="docx",
                                 template="htw-reference.docx",
                                 verbose=True)
dc.construct_command()
dc.convert()


# create template base on docx ref
dc = pandocwrapper.DocxConverter(file_in="example30.docx",
                                 file_out="htw30.pdf",
                                 path_to_files="files/",
                                 verbose=True)
dc.construct_command()
dc.convert()
