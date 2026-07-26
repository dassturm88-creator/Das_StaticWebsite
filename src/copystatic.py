import os
import shutil

def delete_public():
    if os.path.exists("public"):
        shutil.rmtree("public")

def create_public():
    os.mkdir("public")

def copy_static(source, destination):
    for filename in os.listdir(source):
        full_source_path = os.path.join(source, filename)
        if os.path.isfile(full_source_path):
            full_destination_path = os.path.join(destination, filename)
            shutil.copy(full_source_path, full_destination_path)
        else:
            full_destination_path = os.path.join(destination, filename)
            os.mkdir(full_destination_path)            
            copy_static(full_source_path, full_destination_path)