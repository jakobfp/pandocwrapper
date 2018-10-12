import pandocwrapper


bc = pandocwrapper.BaseConverter(file_in="files/example30.docx",
                                 file_out="files/example30.pdf",
                                 from_format=pandocwrapper.docx_str,
                                 verbose=True)

bc.convert()
