import tkinter as tk
from tkinter import filedialog
import time
import json
import os

def openDialogFunction(extension, fileName = 'name'):
    print("Open dialog function")
    root = tk.Tk()
    root.withdraw()

    title = "Open file",
    dirName = None,
    fileExt = extension,
    asFile = False
    fileTypes = [('text files', extension), ('all files', '.*')]
    # define options for opening
    options = {}
    options['defaultextension'] = fileExt
    options['filetypes'] = fileTypes
    options['initialdir'] = dirName
    options['initialfile'] = fileName
    options['title'] = title

    file_path = filedialog.askopenfile(mode='r', **options).name
    if file_path is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        print("No file selected")
        return
    return file_path


def fileSaveWindow(fileName, extension):
    print("Save dialog function")
    root = tk.Tk()
    root.withdraw()

    current_time = time.localtime()
    title = "Save window" + str(extension),
    fileName = str(fileName + '_' + str(current_time[0]) + '-' + str(current_time[1])+ '-' + str(current_time[2]) + "_" + str(
        current_time[3]) + '-' + str(current_time[4]) + '-' + str(current_time[5]))
    dirName = None
    fileExt = extension
    asFile = False
    fileTypes = [('text files', extension), ('all files', '.*')]
    # define options for opening
    options = {}
    options['defaultextension'] = fileExt
    options['filetypes'] = fileTypes
    options['initialdir'] = dirName
    options['initialfile'] = fileName
    options['title'] = title
    file_path = filedialog.asksaveasfile(mode='w', **options)
    if file_path is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        print("No file selected")
        return
    file_path.close()
    print("Saving path: ", str(file_path.name))
    return str(file_path.name)


def fileSavePath(path, toSave, format = ''):
    path_ok = str(path)
    file_path = open(path_ok, "w+")
    """
    for i1 in range(0, len(toSave)):
        for i2 in range(0, len(toSave[i1])):
            toSave[i1][i2] = str(toSave[i1][i2])
        toSave[i1] = ' '.join(toSave[i1])
    toSave = '\n'.join(toSave)
    """
    file_path.writelines(str(toSave))
    file_path.close()  # `()` was missing.

def fileSaveBasic(fileName, toSave,  extension):
    path = fileSaveWindow(fileName, extension)
    fileSavePath(path, toSave)

def saveJson(fileName, data, extension = '.json', thisPath = None, silent = False):
    if silent is False:    print('Saving to json type file')
    if(thisPath is not None):
        path = fileName+extension
    else:
        path = fileSaveWindow(fileName, extension)
    if silent is False: print('Path: ' + path)
    file = open(path, 'w+')
    if silent is False: print(data)
    json.dump(data, file)
    if silent is False: print('Saved properly to json type file')



def loadJson(fileName, extension = '.json', thisPath = None):
    print('Loading from json type file')
    if(thisPath is not None):
        path = thisPath+extension
    else:
        path = openDialogFunction(extension, fileName)
    print(path.split(".")[-1])
    if(path.split(".")[-1] == "log"):
        print("Log format")
        f = open(path)
        data = f.read()
        f.close()
        #print(data)
    else:
        print("Json format")
        print('Path: ' + str(path))
        f = open(path)
        data = json.load(f)
        print(data)
        print('Loaded properly from json type file')
    return data, path

def directoryBox(title=None, dirName=None):
    options = {}
    options['initialdir'] = dirName
    options['title'] = title
    options['mustexist'] = False
    fileName = filedialog.askdirectory(**options)
    if fileName == "":
        return None
    else:
        return fileName

def directoryWindow():
    print("Save dialog function")
    root = tk.Tk()
    root.withdraw()

    current_time = time.localtime()
    title = "Save window folder",
    dirName = None,
    asFile = False
    # define options for opening
    options = {}
    options['initialdir'] = dirName
    options['title'] = title
    options['mustexist'] = False
    file_path = filedialog.askdirectory(**options)
    if file_path is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        print("No file selected")
        return
    print("Saving path: ", str(file_path))
    return str(file_path)

def saveToFolder(data, name = "tmp_file", extension = ".json", folder = "tmp", path = None, silent = False):
    if silent is False:
        print('Save file to folder')
    current_time = time.localtime()
    timeStamp = '_' + str(current_time[0]) + '-' + str(current_time[1]) + '-' + str(
        current_time[2]) + "_" + str(
        current_time[3]) + '-' + str(current_time[4]) + '-' + str(current_time[5])
    dir = os.getcwd() + '\\' + str(folder)
    if os.path.exists(os.path.dirname(dir)) is False:
        if silent is False:
            print('Create directory: ', dir)
        os.makedirs(dir)
    if silent is False:
        print("Folder: ", dir)
    if path is None:
        path = str(dir + '\\' + str(name) + '_date' + timeStamp)
    saveJson(path, data, extension=str(extension), thisPath=True, silent = silent)
    return path