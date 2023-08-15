import os


import os

def search_and_delete_files(folder_path, target_paragraph):
    deleted_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                if target_paragraph in content:
                    deleted_files.append(filename)
                    os.remove(file_path)  # Delete the file
            except UnicodeDecodeError:
                print(f"Error decoding file: {filename}")
            except PermissionError:
                print(f"Permission error for file: {filename} (probably in use by another process)")

    return deleted_files

folder_path = "src/Data Extraction/Dirty Samples"
target_paragraph = "your future career"

deleted_files = search_and_delete_files(folder_path, target_paragraph)

if deleted_files:
    print("Deleted files:")
    for filename in deleted_files:
        print(filename)
    print(f"Total: {len(deleted_files)}")
else:
    print("No files containing the target paragraph were found.")