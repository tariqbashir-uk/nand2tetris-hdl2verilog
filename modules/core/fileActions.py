import sys
import os
import shutil
import hashlib
from shutil import copyfile
from modules.core.logger import Logger
from os import listdir
from os.path import join
from pathlib import Path
from datetime import datetime
#from tzlocal import get_localzone # $ pip install tzlocal

class FileDetails:
    def __init__(self, fileName, path, fileSizeBytes, md5, lastModified):
        self.fileName      = fileName
        self.path          = path
        self.fileSizeBytes = fileSizeBytes 
        self.md5           = md5
        
        if lastModified != None:
            self.lastModified = lastModified.replace(tzinfo=None)    

    def GetAbsoluteFilename(self):
        return os.path.abspath(os.path.join(self.path, self.fileName))

    def GetFilename(self):
        return self.fileName

    def GetFullFilename(self):
        return os.path.join(self.path, self.fileName)

    def GetFullFilenameUnix(self):
        return os.path.join(self.path, self.fileName).replace("\\", "/")

class FileActions:
    def __init__(self):
        self.logger = Logger()

    ##########################################################################
    # IsFile
    ##########################################################################
    def IsFile(self, fileName):
        my_file = Path(fileName)
        return my_file.is_file()   

    ##########################################################################
    # IsExecutable
    ##########################################################################
    def IsExecutable(self, fileName):
        return os.access(fileName, os.X_OK)    
       
    ##########################################################################
    # Rename
    ##########################################################################
    def Rename(self, srcFolder, dstFolder):
        os.rename(srcFolder, dstFolder)

    ##########################################################################
    # MoveFolder
    ##########################################################################
    def MoveFolder(self, srcFolder, dstFolder):
        shutil.move(srcFolder, dstFolder)
        # Unlike os calls which are blocking we have to wait until rmtree 
        # completes. We do this by waiting until the folder no longer exists.
        while os.path.exists(srcFolder): # check if it exists
                pass

    @staticmethod
    ##########################################################################
    # GetFileNameAndExt
    ##########################################################################
    def GetFileNameAndExt(fileName):
        return os.path.splitext(fileName)  

    ##########################################################################
    # GetAbsoluteFilename
    ##########################################################################
    def GetAbsoluteFilename(self, relativeFilename):
        return os.path.abspath(relativeFilename)

    ##########################################################################
    # CreateFolderIfNeeded
    ##########################################################################
    def CreateFolderIfNeeded(self, folder):
        if not self.DoesFolderExist(folder):
            os.makedirs(folder)

    ##########################################################################
    # DoesFolderExist
    ##########################################################################
    def DoesFolderExist(self, folder):
        return os.path.exists(folder)

    ##########################################################################
    # DoesFileExist
    ##########################################################################
    def DoesFileExist(self, fileName):
        my_file = Path(fileName)
        return my_file.is_file()

    ##########################################################################
    # GetNumFilesInFolder
    ##########################################################################
    def GetNumFilesInFolder(self, folder, ext = None):
        if self.DoesFolderExist(folder) == True:
            files = [f for f in os.scandir(folder) if f.is_file()]
            if ext != None:
                files = [k for k in files if ext in k.name]
            return len(files)
        else:
            return 0            

    ##########################################################################
    # DeleteFile
    ##########################################################################
    def DeleteFile(self, fileName):
        if self.DoesFileExist(fileName):
            try:
                my_file = Path(fileName)
                my_file.unlink()
            except Exception as e:
                self.logger.Error(str(e))

    ##########################################################################
    # DeleteFolder
    ##########################################################################
    def DeleteFolder(self, folderName):
        if self.DoesFolderExist(folderName):
            try:
                self.DeleteFilesInFolder(folderName)
                self.RemoveFolder(folderName)
            except Exception as e:
                self.logger.Error(str(e))

    ##########################################################################
    # DeleteFilesInFolder
    ##########################################################################
    def DeleteFilesInFolder(self, folderName):
        if self.DoesFolderExist(folderName) == True:
            for the_file in os.listdir(folderName):
                file_path = os.path.join(folderName, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path): 
                        self.RemoveFolder(file_path)
                except Exception as e:
                    self.logger.Error(str(e))

    ##########################################################################
    # RemoveFolder
    ##########################################################################
    def RemoveFolder(self, folderName):
       if self.DoesFolderExist(folderName) == True:
        shutil.rmtree(folderName)
        # Unlike os calls which are blocking we have to wait until rmtree 
        # completes. We do this by waiting until the folder no longer exists.
        while os.path.exists(folderName): # check if it exists
            pass

    ##########################################################################
    # GetFoldersFromEndPath
    ##########################################################################
    def GetFoldersFromEndPath(self, path, numberToRemove):
        name = ""
        head = path
        for i in range(0, numberToRemove):
            head, tail = os.path.split(head)
            name = join(tail, name)

        return name    

    ##########################################################################
    # GetFoldersFromEndPathUntil
    ##########################################################################
    def GetFoldersFromEndPathUntil(self, path, nameToStopAt):
        name  = ""
        head  = path
        tail  = ""
        found = True
        while tail != nameToStopAt:
            newhead, tail = os.path.split(head)
            name = join(tail, name)

            if newhead != head:
                head = newhead
            else:
                # This stops an infinite loop if nameToStopAt is not in path
                found = False
                break

        return name[:-1], found   

    ##########################################################################
    # CopyFile
    ##########################################################################
    def CopyFile(self, srcFileName, dstFileName):
        copyfile(srcFileName, dstFileName)        
        # Unlike os calls which are blocking we have to wait until rmtree 
        # completes. We do this by waiting until the folder no longer exists.
        while self.DoesFileExist(dstFileName) != True: # check if it exists
            pass

    ##########################################################################
    # GetFileDetailsInFolder
    ##########################################################################
    def GetFileDetailsInFolder(self, folder):
        fileDetails = []
        for path, _, files in os.walk(folder):
            for file in files:
                fileDetail = FileDetails(file, path, 0, "", None)

                fileDetail.fileSizeBytes = os.path.getsize(fileDetail.GetAbsoluteFilename()) 
                fileDetail.md5           = self._md5(fileDetail.GetAbsoluteFilename(), fileDetail.fileSizeBytes) 

                fileDetails.append(fileDetail)

        return fileDetails

    ##########################################################################
    # GetFilesWithExtInFolder
    ##########################################################################
    def GetFilesWithExtInFolder(self, folder, extension):
        files = [f for f in listdir(folder) if os.path.isfile(join(folder, f))]
        files = [k for k in files if extension in k]
        return files

    ##########################################################################
    # GetFileModDate
    ##########################################################################
    def GetFileModDate(self, filename):
        try:
            mtime = os.path.getmtime(filename)
        except OSError:
            # Use 86400 and not 0 so compatible with windows.
            mtime = 86400
        return datetime.fromtimestamp(mtime)

    ##########################################################################
    # IsFileNewerThan
    ##########################################################################
    def IsFileNewerThan(self, filename1, filename2):
        file1 = self.GetFileModDate(filename1)
        file2 = self.GetFileModDate(filename2)
        #print(filename1 + " = " + str(file1))
        #print(filename2 + " = " + str(file2))
        return file1 > file2 

    ##########################################################################
    # Private: _md5
    ##########################################################################
    def _md5(self, fileName, fileSizeBytes):
        hash_md5 = hashlib.md5()
        if fileSizeBytes > 20000000:
            with open(fileName, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        else:
            with open(fileName, "rb") as f:
                hash_md5 = hashlib.md5(f.read())

        return hash_md5.hexdigest()      