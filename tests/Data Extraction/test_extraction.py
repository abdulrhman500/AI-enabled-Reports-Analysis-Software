path =   r""
#for decoding
import codecs
#using Textract
import textract
#extract text in byte format
textract_text = textract.process(path)
#convert bytes to string
textract_str_text = codecs.decode(textract_text)
print(textract_str_text)