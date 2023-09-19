import pandas as pd
import glob
import os

folder_path = '' # add here your folder path
file_list = glob.glob(folder_path + "/*.txt")
dir_list = os.listdir(folder_path)

output = pd.DataFrame({'name':[],'text':[]})

# loop over raw text files to create the dataframe
for i in range(0,len(file_list)):
    with open(file_list[i], 'r', encoding='latin-1') as f:
      text = f.read().replace('\n', '')
      new_row = {'name':file_list[i],'text':text}
    output = pd.concat([output, pd.DataFrame([new_row])], ignore_index=True)