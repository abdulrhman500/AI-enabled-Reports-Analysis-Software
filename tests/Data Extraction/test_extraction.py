path =   r"C:\\Users\\hoda2\\Downloads\\Unscanned\\Anas ElNemr (46-6226) - Anas Nemr.pdf"
#for decoding
import codecs
#using Textract
import textract
#extract text in byte format
textract_text = textract.process(path)
#convert bytes to string
textract_str_text = codecs.decode(textract_text)
print(textract_str_text)