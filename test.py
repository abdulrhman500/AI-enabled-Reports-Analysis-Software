path = r""

import fitz  # this is pymupdf
doc = fitz.open(path)
pymupdf_text = ""
for page in doc:
    pymupdf_text += page.get_text(sort ='true')
print(pymupdf_text)