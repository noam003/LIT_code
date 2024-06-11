# Noa M
# intial code for seperating files from the original LibriSpeech
# database to a local file for our database
import os

full_txt = "/Users/noamargolin/Downloads/LibriSpeech/dev-clean/3853/163249/3853-163249.trans.txt"
# opening file
file1 = open(full_txt, 'r')
Lines = file1.readlines()

# creating new folder
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
new_folder_name = '3853'
new_folder_path = os.path.join(desktop_path, new_folder_name)
os.makedirs(new_folder_path, exist_ok=True)

# adding txt file line by line
for line in Lines:
    split_string = line.split(' ', 1)
    txt_name = split_string[0][-4:]
    new_file_path = os.path.join(new_folder_path, txt_name)
    with open(new_file_path, 'w') as file:
        file.write(split_string[1])