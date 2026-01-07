import os
import shutil

def copy_files_recursive(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
    
    for filename in os.listdir(source_dir):
        from_path = os.path.join(source_dir, filename)
        destination_path = os.path.join(source_dir, filename)
        print(f" * {from_path} -> {destination_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, destination_path)
        else:
            copy_files_recursive(from_path, destination_path)