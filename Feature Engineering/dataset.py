import pandas as pd
import glob
import os

folder_path = 'C:\\Users\\hoda2\\Documents\\NLP Internship\\Final Samples'
file_list = glob.glob(folder_path + "/*.txt")
dir_list = os.listdir(folder_path)

output = pd.DataFrame({'name':[],'text':[]})
for i in range(0,len(file_list)):
    with open(file_list[i], 'r', encoding='latin-1') as f:
      text = f.read().replace('\n', '')
      new_row = {'name':file_list[i],'text':text}
    output = pd.concat([output, pd.DataFrame([new_row])], ignore_index=True)
    # output = output.append(new_row, ignore_index=True)

pd.set_option('display.max_rows', None)
print(output.head())
# output.shape
# print(output.size)