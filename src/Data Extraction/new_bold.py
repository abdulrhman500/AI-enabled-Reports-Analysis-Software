import pdfplumber
file_to_parse = "E:\\NLP\\Internship\\Dirty Reports\\Dirty Files\\correct template\\(A) 1-merged - Rawan Ahmad.pdf"
with pdfplumber.open(file_to_parse) as pdf: 
    text = pdf.pages[3]
    clean_text = text.filter(lambda obj: not (obj["object_type"] == "char" and "Bold" in obj["fontname"]))
    print(clean_text.extract_text())

