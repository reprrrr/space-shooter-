import os
def get_files_names(path, extension):
    names = []
    for file in os.listdir(path):
        file_name = os.fsdecode(file)
        if file_name.endswith(extension):
            names.append(file_name[:-len(extension)])
    return names