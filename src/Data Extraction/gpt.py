
import os
import re
import PyPDF2
import openai  # Import the openai library

# Set your OpenAI API key
openai.api_key = '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'

# Directory containing the PDF files
pdf_directory = "D:/A-erasi/testUnscanned"
output_directory = "D:/A-erasi/test results"  # Directory to save the text files

#Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through each PDF in the directory
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, pdf_file)

        # Extract text from the PDF using PyPDF2
        with open(pdf_path, "rb") as pdf:
            pdf_reader = PyPDF2.PdfReader(pdf)
            pdf_content = "\n".join([page.extract_text() for page in pdf_reader.pages])

        # Compose a prompt for GPT-3
        prompt = f"Extract the information about the performed tasks for this report:\n{pdf_content}"

        # Make an API call to GPT-3
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=300
        )

        # Extracted response
        extracted_information = response.choices[0].text

        # Save the response to a text file
        output_filename = os.path.splitext(pdf_file)[0] + ".txt"
        output_path = os.path.join(output_directory, output_filename)
        with open(output_path, "w") as output_file:
            output_file.write(extracted_information)
