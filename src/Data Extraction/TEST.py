import os
i = 0
def check_txt_files(folder_path, min_chars=100):
    # Ensure the folder path is valid
    global i
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path!")

    # List all files in the folder
    file_list = os.listdir(folder_path)

    for filename in file_list:
        # Check if the file has a .txt extension
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            # Open the file with explicit UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Check the number of characters in the file
            num_chars = len(content.split())
            if num_chars >= min_chars:
                # print(f"File '{filename}' has {num_chars} characters (>= {min_chars} characters).")
                pass
            else:
                i=i+1
                print(f"File '{filename}' has {num_chars} words (< {min_chars} words).")


folder_path = "src\Data Extraction\Dirty Samples"
check_txt_files(folder_path)
print(i)