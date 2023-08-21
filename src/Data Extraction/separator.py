import os
import shutil

# Paths to directories and files
input_directory_path = "D:/A-erasi/folders"
output_directory_path = "D:/A-erasi/trashCollection"
pdf_list_file = "D:/A-erasi/trash.txt"
pdf_extension = ''

# Read the list of PDF file names from the text file
with open(pdf_list_file, 'r') as f:
    pdf_file_names = f.read().splitlines()

# Filter PDF files from the input directory and move them to the output directory
for pdf_file_name in pdf_file_names:
    source_pdf_path = os.path.join(input_directory_path, pdf_file_name + pdf_extension)
    target_pdf_path = os.path.join(output_directory_path, pdf_file_name + pdf_extension)

    # Check if the PDF file exists in the source directory
    if os.path.exists(source_pdf_path) and source_pdf_path.lower().endswith(pdf_extension):
        # Move the PDF file to the output directory
        shutil.move(source_pdf_path, target_pdf_path)
        print(f"Moved {pdf_file_name + pdf_extension} to {output_directory_path}")
    else:
        print(f"PDF file {pdf_file_name + pdf_extension} not found in {input_directory_path}")

pdf_extension = '.pdf'

# Walk through the input directory and its subdirectories
# for root, dirs, files in os.walk(input_directory_path):
#     for filename in files:
#         if filename.lower().endswith(pdf_extension):
#             source_pdf_path = os.path.join(root, filename)
#             target_pdf_path = os.path.join(input_directory_path, filename)

#             # Move the PDF file to the output directory
#             shutil.move(source_pdf_path, target_pdf_path)
#             print(f"Moved {filename} to {output_directory_path}")