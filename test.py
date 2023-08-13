path = r"C:\\Users\\hoda2\\Downloads\\Not Bold but following template\\Danial Amir Ayad 46-2078.pdf"

import fitz  # this is pymupdf
doc = fitz.open(path)
pymupdf_text = ""
for page in doc:
    pymupdf_text += page.get_text(sort ='true')
print(pymupdf_text)