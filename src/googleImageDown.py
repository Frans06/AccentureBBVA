import os
from google_images_download import google_images_download   #importing the library
import shutil
from os import listdir
from os.path import isfile, join


def down(name):
    name = "\'" + name + "\'"
    path = 'downloads/' + name
    response = google_images_download.googleimagesdownload()   #class instantiation
    arguments = {"keywords":name,"limit":5,"urls":False}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    files = [f for f in listdir(path) if isfile(join(path, f))]
    x = 1
    tmp_path = '/root/tmp/'
    tmp_files = [f for f in listdir(tmp_path) if isfile(join(tmp_path, f))]
    for y in tmp_files:
        os.remove(tmp_path + y)
    name = name.replace(' ','')
    for file in files:

        shutil.move(path + '/' + file, '/root/tmp/' +  str(x) +  '_' + name[1:-1] +  file[-4:])
        x += 1
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        os.remove(path + '/' + file)

if __name__ == '__main__' :
    down('Juan Andres viera medina')
