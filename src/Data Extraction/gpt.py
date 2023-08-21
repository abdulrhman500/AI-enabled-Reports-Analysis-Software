
import os
import re
import PyPDF2
import openai  # Import the openai library
import extract_unscanned_pdf
import pdfplumber
import fitz
import shutil
import time


# Set your OpenAI API key
openai.api_key = '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'

# Directory containing the PDF files
pdf_directory = "D:/A-erasi/trashCollection"
output_directory = "D:\A-erasi\playground"  # Directory to save the text files
move_directory = "D:\A-erasi\done"
#Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through each PDF in the directory
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, pdf_file)

        # Extract text from the PDF using PyPDF2
        print("opening file "+os.path.splitext(pdf_file)[0])
        with fitz.open(pdf_path) as doc:  # open document
            pdf_content = chr(12).join([page.get_text() for page in doc])
        # print(pdf_content)    
        pdf_content = pdf_content.encode("utf-8")
        # print(pdf_content)
        # Compose a prompt for GPT-3
        prompt = f"Extract the information about the performed tasks for this report:\n{pdf_content}"

        # Make an API call to GPT-3
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role":"user","content":prompt}],
            max_tokens=600
        )

    #comparing different parsing libraries
        
        # with open(pdf_path, "rb") as pdf:
        #     pdf_reader = PyPDF2.PdfReader(pdf)
        #     pdf_content = "\n".join([page.extract_text() for page in pdf_reader.pages])

        # print("PyPDF2 extraction " + pdf_content)
        # x = extract_unscanned_pdf.get_text(pdf_path)
        # print("uscanned extraction /n "+ x)

        # with pdfplumber.open(pdf_path) as pdf:
        #     pdf_content2 = "\n".join([page.extract_text() for page in pdf.pages])
        # print("plumber extraction "+ pdf_content2 )

        # print("starting fitz")
        # with fitz.open(pdf_path) as doc:  # open document
        #     pdf_content3 = chr(12).join([page.get_text() for page in doc])
        # print("PyMuPDF extraction "+ pdf_content3 )
        # save = "pypdf2 extraction \n"+pdf_content+"\n"+"unscanned \n"+x+"\n" + "plumber \n"+pdf_content2+"\n"+"fitz \n"+pdf_content3
        # output_path = os.path.join(output_directory, "result.txt")
        # with open(output_path, "w") as output_file:
        #     output_file.write(save)
        # print("response saved for "+"result")

        # Extracted response
        extracted_information = response.choices[0].message.content
        # print(extracted_information)
        # Save the response to a text file
        output_directory_with_body = "D:/A-erasi/resultsWithBody"
        output_filename = os.path.splitext(pdf_file)[0] + ".txt"
        output_path = os.path.join(output_directory, output_filename)
        output_path_with_body = os.path.join(output_directory_with_body, output_filename)
        file_content = f"extracted data:\n{pdf_content}\n response result:\n {extracted_information}"
        with open(output_path, "w") as output_file:
            output_file.write(extracted_information)
        with open(output_path_with_body, "w") as output_file:
            output_file.write(file_content)
        print("response saved for "+output_filename)
        target_pdf_path = os.path.join(move_directory, os.path.splitext(pdf_file)[0] + ".pdf")

        shutil.move(pdf_path, target_pdf_path)
        # time.sleep(9)
        # print(file_content)
