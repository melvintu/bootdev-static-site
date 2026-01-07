import os
import shutil
from copystatic import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)



"""
Over-engineered with some bugs of if source in abs_file_path (too generic of a check)

def source_to_destination(root, source, destination, clean=True):
    if clean:
        if os.path.exists(destination):
            shutil.rmtree(destination)

    os.makedirs(destination, exist_ok=True)

    abs_file_path = os.path.abspath(root)
    all_files = os.listdir(abs_file_path)
    for file in all_files:
        if source in abs_file_path:
            if os.path.isfile(os.path.join(abs_file_path, file)):
                shutil.copy(os.path.join(abs_file_path, file), destination)
            else:
                source_to_destination(os.path.join(abs_file_path, file), source, destination+"/"+file, False)
        elif not os.path.isfile(os.path.join(abs_file_path, file)):
            source_to_destination(os.path.join(abs_file_path, file), source, destination, False)
"""

if __name__ == "__main__":
    main()