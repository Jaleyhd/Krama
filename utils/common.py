"""
    This module deals with job related manipulations. In expresso, job is
understood as a subtask which needs to be performed to get expected result.
Job config is a file which gives you complete information related to this
subtask.

"""
from __future__ import absolute_import
from google.protobuf import text_format
import os
import subprocess

def get_folders(main_folder=None):
    #Check if folder is unintiallized
    if main_folder is None:
        raise Exception("Call with main folder Path")
    #Check if main folder is empty
    if main_folder is "" :
        raise Exception("Empty main folder path")

    dir_list = [os.path.join(main_folder, folder)
                for folder in os.listdir(main_folder)
                if os.path.isdir(os.path.join(main_folder, folder)) and not folder.startswith('.')]

    #Check if main folder has any subfolders
    if len(dir_list)==0 :
        raise Exception("Add job directories in main folder")

    return [elem.strip().split('/')[-1] for elem in dir_list ]

def compile_core_config(krama_root=None):
    subprocess.call("protoc -I "+krama_root+'/proto --python_out='
                    +krama_root+'/src/expresso/proto '+krama_root+'/proto/expresso.proto',shell=True)



def compile_configs(dir_list=None,krama_root=None):
    if krama_root is None :
        raise Exception("Expresso root not Initialized")
    if dir_list is None :
        raise Exception("Uninitialized Directory List")
    for elem in dir_list:
        print elem


def is_empty_filename(file_path):
    if len(file_path.strip().split("/")[-1])==0:
        return True
    else:
        return False

def get_file_path(config_path,path_specified):
    if path_specified=="":
        raise Exception("Empty File Name")
    if path_specified.startswith("./") and not is_empty_filename(path_specified):
        return config_path+path_specified[1:]
    if path_specified.startswith("../") and not is_empty_filename(path_specified):
        return config_path+"/"+path_specified
    if path_specified.startswith('/'): return path_specified;
    return config_path+'/'+path_specified





if __name__== "__main__":
    compile_core_config('/usr/share/expresso')