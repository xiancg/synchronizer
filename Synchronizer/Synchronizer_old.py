# -*- coding: utf-8 -*-
'''
Library to copy and compare files and directories.

Created on Mar 25, 2015

@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/

TODO:
-Agregar opcion para force Overwrite, que sea opcional
'''


# --------------------------------------------------------------------------------------------
# imports
# --------------------------------------------------------------------------------------------
import os
import time
import shutil

# --------------------------------------------------------------------------------------------
# Metadata
# --------------------------------------------------------------------------------------------
__author__ = "Chris Granados"
__copyright__ = "Copyright Chris Granados"
__credits__ = ["Chris Granados"]
__version__ = "2.0.0"
__email__ = "chris.granados@xiancg.com"


# --------------------------------------------------------------------------------------------
# Class: Synchronizer
# --------------------------------------------------------------------------------------------
class Synchronizer():
    '''
    Object to copy and compare files and directories.

    -You can print the log (it's a multi line string) by printing the instanced object itself
    -You can access the log list by the property Synchronizer.log
    -statusDict: You can change the text it returns on getSyncStatus by setting the property
    statusDict {1: "In sync",
             2: "Out of sync",
             3: "Same date, different size",
             4: "Different date, same size",
             5: "Both paths missing",
             6: "Source file missing",
             7: "Target file missing",
             8: "Different kind of paths (file-dir, dir-file)"}

    Attributes:
        parentUI (QtGui.QWidget): QtGui.QWidget that uses this tool instance. Default=None

    Properties:
        log(list): List containing a array of string descriptions of all actions executed by Synchronizer instance.
        statusDict: Eight possible status options used by getSyncStatus to return
        activateLog: False by default. Set to True if you want to debug Synchronizer actions.
        forceOverwrite: False by default. Set to True if you want to make sure all operations override existing files
            and directories if found.
    '''
    # --------------------------------------------------------------------------------------------
    # Constructor
    # --------------------------------------------------------------------------------------------
    def __init__(self, _parentUI=None):
        '''
        Compares given files or directories. Copies files, textures, sequences.
        :param _parentUI: QtGui.QWidget that uses this tool instance. Default=None
        :type _parentUI: QtGui.QWidget
        '''
        self.parentUI = _parentUI
        self.__statusDict = {1: "In sync",
                             2: "Out of sync",
                             3: "Same date, different size",
                             4: "Different date, same size",
                             5: "Both paths missing",
                             6: "Source file missing",
                             7: "Target file missing",
                             8: "Different kind of paths (file-dir, dir-file)"}
        self.__forceOverwrite = False
        self.__activateLog = False
        self.__log = []

    # --------------------------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------------------------
    def getSyncStatus(self, _srcPath, _trgPath):
        '''
        Compares two given files and returns a status
        :param _srcPath: Path to a file or directory
        :type _srcPath: string
        :param _trgPath: Path to a file or directory
        :type _trgPath: string
        :return: Result of comparing both files, including if something was not found.
        :rtype: string
        '''
        if os.path.exists(_srcPath) and os.path.exists(_trgPath):
            srcTime = time.ctime(os.path.getmtime(_srcPath))
            trgTime = time.ctime(os.path.getmtime(_trgPath))
            srcSize = os.path.getsize(_srcPath)
            trgSize = os.path.getsize(_trgPath)
            if os.path.isdir(_srcPath) and os.path.isdir(_trgPath):
                srcSize = self.getDirSize(_srcPath)
                trgSize = self.getDirSize(_trgPath)
            # In sync
            if srcTime == trgTime and srcSize == trgSize:
                return self.statusDict[1]
            # Out of sync
            elif srcTime != trgTime and srcSize != trgSize:
                return self.statusDict[2]
            # Same date, different size
            elif srcTime == trgTime and srcSize != trgSize:
                return self.statusDict[3]
            # Different date, same size
            elif srcTime != trgTime and srcSize == trgSize:
                return self.statusDict[4]
        # Both paths missing
        elif not os.path.exists(_srcPath) and not os.path.exists(_trgPath):
            return self.statusDict[5]
        # Source path missing
        elif not os.path.exists(_srcPath):
            return self.statusDict[6]
        # Target path missing
        elif not os.path.exists(_trgPath):
            return self.statusDict[7]
        # Different kind of paths (file-dir)
        elif os.path.isfile(_srcPath) and os.path.isdir(_trgPath):
            return self.statusDict[8]
        # Different kind of paths (dir-file)
        elif os.path.isdir(_trgPath) and os.path.isfile(_srcPath):
            return self.statusDict[8]
        # Fail
        else:
            return "Failed to find status."

    def getDirSize(self, _path):
        '''
        Get the total size of files and sub-directories for given path.
        :param _path: Path to a directory
        :type _path: string
        :return: Sum of file and sub-directories sizes
        :rtype: float. None if _path is not a directory.
        '''
        if os.path.isdir(_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return total_size
        else:
            return None

    def getSequenceFiles(self, _path):
        '''
        Given a file path, find all sibling files for the sequence.
        :param _path: Path to a file. Ex= X:/Files/render/RND_beauty.0001.exr
        :type _path: string
        :return: List of files (full paths) with the same name pattern in the given directory
        :rtype: list
        '''
        sequenceBool, namePattern, fileExt, parentFolder, hashStr = self.isSequence(_path)

        # Fix get sequence of a single file, resultin in a pattern of 0 length
        if len(namePattern) == 0:
            singleFile = [_path]
            return singleFile

        if sequenceBool:
            self.__logAppend("Name pattern for given sequence is: {}{}.{}".format(namePattern, hashStr, fileExt))
            # Build list of files with the same name structure in the directory
            filesAndDirs = os.listdir(parentFolder)
            preFileList = []
            for each in filesAndDirs:
                if os.path.isfile(os.path.join(parentFolder, each)):
                    preFileList.append(each)
            fileList = []
            for each in preFileList:
                thisFileExt = self._getFileExtension(each)
                if each[:len(namePattern)] == namePattern and thisFileExt == fileExt:
                    fileList.append(parentFolder + "/" + each)

        return fileList

    def isSequence(self, _path):
        '''
        Tests if given file path has siblings.
        :param _path: Path to a file. Ex= X:/Files/render/RND_beauty.0001.exr
        :type _path: string
        :return: sequenceBool: True if siblings found. False if file is unique in that directory.
        :rtype: bool
        :return: namePattern: Base file name used for sibling files.
        :rtype: string
        :return: fileExt: File extension for sibling files.
        :rtype: string
        :return: parentFolder: Parent folder that contains all given sibling files.
        :rtype: string
        :return: hasStr: Number of digits, represented as '#' characters found in the name pattern for sibling files.
        :rtype: string
        '''
        pathParts = _path.rsplit("/", 1)
        parentFolder = pathParts[0]
        fileWithExt = pathParts[1]
        # Split extension
        fileName, fileExt = fileWithExt.rsplit(".", 1)
        # Get number of digits
        digitsNumber = 0
        for each in fileName[::-1]:
            if each.isdigit() or each == '#':
                digitsNumber += 1
            else:
                break
        namePattern = fileName[:-digitsNumber]
        hashStr = "#" * digitsNumber
        # Find other files with the same name structure in the directory
        filesAndDirs = os.listdir(parentFolder)
        sequenceBool = False
        for each in filesAndDirs:
            eachPath = os.path.join(parentFolder, each)
            if "\\" in eachPath:
                eachPath = eachPath.replace("\\", "/")
            if os.path.isfile(eachPath):
                thisFileExt = self._getFileExtension(each)
                if _path == eachPath:
                    continue
                elif each[:len(namePattern)] == namePattern and thisFileExt == fileExt:
                    sequenceBool = True
                    break
        return sequenceBool, namePattern, fileExt, parentFolder, hashStr

    def processPaths(self, _srcPath, _trgPath, **kwargs):
        '''
        Copies a file, texture (with .tx), file sequence (with .tx)
            or directory from _srcPath to _trgPath
        Sequence requires passing the full path to one file
            from the sequence for both source and target.
        Source and target must be same type (Both files or directories).
        For UDIMs use isSequence=True.
        :param _srcPath: Full path to a file or directory
        :type _srcPath: string
        :param _trgPath: Full path to a desired file or directory final location
        :type _trgPath: string
        :param kwargs:
            includeTX = True to copy all .tx found that match the given file
            onlyTX  = True to skip non tx files on copy
        :return: True if successful.
        :rtype: boolean
        '''
        # Change backslash for slash
        if "\\" in _srcPath:
            _srcPath = _srcPath.replace("\\", "/")
        if "\\" in _trgPath:
            _trgPath = _trgPath.replace("\\", "/")

        # Check if source path is dir or file
        passedDirs = False
        if os.path.isdir(_srcPath):
            passedDirs = True

        # Sanity check
        if _srcPath == _trgPath:
            self.__logAppend("Source and target are the same, it will be skipped: {}".format(_srcPath))
            return False
        elif not os.path.exists(_srcPath):
            self.__logAppend("Source file doesn't exist, it will be skipped: {}".format(_srcPath))
            return False
        elif passedDirs:
            result = self.__processDirs(_srcPath, _trgPath)
            self.__logAppend("Finished processing directories: {} and {}".format(_srcPath, _trgPath))
            return result
        else:
            result = self.__processFiles(_srcPath, _trgPath, kwargs)
            self.__logAppend("Finished processing files: {} and {}".format(_srcPath, _trgPath))
            return result

    def getRangeFromSequence(self, _filename):
        '''
        Receives a file, convert it to sequence, and get first a last number of that sequence
        Args:
            _filename (string) File to scan
        Return:
            list of two values (first frame a last)
        '''
        sequence = self.getSequenceFiles(_filename)
        firstFrame = sequence[0]
        lastFrame = sequence[-1]
        firstFrame = os.path.splitext(firstFrame)[0]
        lastFrame = os.path.splitext(lastFrame)[0]
        try:
            firstFrame = int(firstFrame.split('.')[-1])
        except ValueError:
            try:
                firstFrame = int(firstFrame.split('_')[-1])
            except ValueError:
                firstFrame = '####'
        try:
            lastFrame = str(int(lastFrame.split('.')[-1]))
        except ValueError:
            try:
                lastFrame = str(int(lastFrame.split('_')[-1]))
            except ValueError:
                lastFrame = '####'

        firstFrame = str(firstFrame)
        lastFrame = str(lastFrame)
        return [firstFrame.zfill(4), lastFrame.zfill(4)]

    def __processDirs(self, _srcPath, _trgPath):
        '''
        Copies a directory from _srcPath to _trgPath
        :param _srcPath: Full path to a file
        :type _srcPath: string
        :param _trgPath: Full path to a desired file final location
        :type _trgPath: string
        :return: True if successful.
        :rtype: boolean
        '''
        exists = os.path.exists(_trgPath)
        # Create folder structure
        try:
            if not exists:
                shutil.copytree(_srcPath, _trgPath)
                self.__logAppend("Copied {} to {}".format(_srcPath, _trgPath))
                return True
            elif exists and self.forceOverwrite:
                shutil.rmtree(_trgPath)
                shutil.copytree(_srcPath, _trgPath)
                self.__logAppend("Overwrote {} with {}".format(_srcPath, _trgPath))
                return True
            else:
                self.__logAppend("Directory already existed and forceOverwrite is set to False: {}".format(_trgPath))
                return False
        except IOError:
            self.__logAppend("The specified source doesn't exist: {}".format(_srcPath))
            return False

    def __processFiles(self, _srcPath, _trgPath, kwargs):
        '''
        Copies a file, texture (with .tx), file sequence (with .tx) from _srcPath to _trgPath
        Sequence requires passing the full path to one file from the sequence.
        For UDIMs use isSequence=True.
        :param _srcPath: Full path to a file
        :type _srcPath: string
        :param _trgPath: Full path to a desired file final location
        :type _trgPath: string
        :param kwargs:
            includeTX = True to copy all .tx found that match the given file
            onlyTX = True to copy only .tx files found that match the given file
        :type kwargs: dict
        :return: True if successfully copied even if it couldn't copy TX files.
        :rtype: boolean
        '''
        if "onlyTX" in kwargs.keys():
            skipNonTx = kwargs["onlyTX"]
        else:
            skipNonTx = False

        pathParts = _trgPath.rsplit("/", 1)
        finalFolder = pathParts[0]

        sequenceBool = self.isSequence(_srcPath)[0]
        if sequenceBool:
            trgFolderPath = _trgPath.rsplit("/", 1)[0]
            # Build list of files with the same name structure in the directory
            fileList = self.getSequenceFiles(_srcPath)

            # Create folder structure
            if not os.path.exists(trgFolderPath):
                try:
                    os.makedirs(trgFolderPath)
                    self.__logAppend("Directory structure created: {}".format(trgFolderPath))
                except WindowsError:
                    self.__logAppend("Directory structure couldn't be created: {}".format(_trgPath))
                    return False
            else:
                self.__logAppend("Directory structure already existed: {}".format(finalFolder))

            # Copy files
            for each in fileList:
                # Copy Only .tx
                if not skipNonTx:
                    try:
                        seqFileName = each.rsplit("/", 1)[1]
                        exists = os.path.exists(trgFolderPath + '/' + seqFileName)
                        if not exists:
                            shutil.copy2(each, trgFolderPath)
                            self.__logAppend("Copied {} to {}".format(each, trgFolderPath))
                        elif exists and self.forceOverwrite:
                            shutil.copy2(each, trgFolderPath)
                            self.__logAppend("Copied {} to {}".format(each, trgFolderPath))
                        else:
                            self.__logAppend("File already existed and forceOverwrite is set to False: {}".format(trgFolderPath + '/' + seqFileName))
                    except IOError:
                        self.__logAppend("The specified source doesn't exist: {}".format(each))
                        return False

                # Copy .tx
                if "includeTX" in kwargs.keys():
                    if kwargs["includeTX"]:
                        txPath = each.rsplit(".", 1)[0] + ".tx"
                        srcExists = os.path.exists(txPath)
                        if srcExists:
                            try:
                                txFileName = txPath.rsplit("/", 1)[1]
                                exists = os.path.exists(trgFolderPath + '/' + txFileName)
                                if not exists:
                                    shutil.copy2(txPath, trgFolderPath)
                                    self.__logAppend("Copied {} to {}".format(txPath, trgFolderPath))
                                elif exists and self.forceOverwrite:
                                    shutil.copy2(txPath, trgFolderPath)
                                    self.__logAppend("Copied {} to {}".format(txPath, trgFolderPath))
                                else:
                                    self.__logAppend("File already existed and forceOverwrite is set to False: {}".format(
                                                    trgFolderPath + '/' + txFileName))
                            except IOError:
                                self.__logAppend("The specified source TX file doesn't exist: {}".format(txPath))
                        else:
                            self.__logAppend("The specified source TX file doesn't exist: {}".format(txPath))
            return True
        else:
            # Create folder structure
            if not os.path.exists(finalFolder):
                try:
                    os.makedirs(finalFolder)
                    self.__logAppend("Directory structure created: {}".format(finalFolder))
                except WindowsError:
                    self.__logAppend("Directory structure couldn't be created: {}".format(finalFolder))
                    return False
            else:
                self.__logAppend("Directory structure already existed: {}".format(finalFolder))

            # Copy single files

            # Copy Only .tx
            if not skipNonTx:
                try:
                    fileName = pathParts[1]
                    exists = os.path.exists(finalFolder + '/' + fileName)
                    if not exists:
                        shutil.copy2(_srcPath, finalFolder)
                        self.__logAppend("Copied {} to {}".format(_srcPath, finalFolder))
                    elif exists and self.forceOverwrite:
                        shutil.copy2(_srcPath, finalFolder)
                        self.__logAppend("Copied {} to {}".format(_srcPath, finalFolder))
                    else:
                        self.__logAppend("File already existed and forceOverwrite is set to False: {}".format(finalFolder + '/' + fileName))
                except IOError:
                    self.__logAppend("The specified source doesn't exist: {}".format(_srcPath))
                    return False
            # Copy .tx
            if "includeTX" in kwargs.keys():
                if kwargs["includeTX"]:
                    txPath = _srcPath.rsplit(".", 1)[0] + ".tx"
                    srcExists = os.path.exists(txPath)
                    if srcExists:
                        try:
                            txFileName = txPath.rsplit("/", 1)[1]
                            exists = os.path.exists(finalFolder + '/' + txFileName)
                            if not exists:
                                shutil.copy2(txPath, finalFolder)
                                self.__logAppend("Copied {} to {}".format(txPath, finalFolder))
                            elif exists and self.forceOverwrite:
                                shutil.copy2(txPath, finalFolder)
                                self.__logAppend("Copied {} to {}".format(txPath, finalFolder))
                            else:
                                self.__logAppend("File already existed and forceOverwrite is set to False: {}".format(
                                                finalFolder + '/' + txFileName))
                        except IOError:
                            self.__logAppend("The specified source TX file doesn't exist: {}".format(txPath))
                    else:
                        self.__logAppend("The specified source TX file doesn't exist: {}".format(txPath))
            return True

    def _getFileExtension(self, filename):
        ''' Returns extension of this file with no '.' '''
        thisFileExt = os.path.splitext(filename)[1]
        # If the file has no extension, make it null
        if len(thisFileExt) > 0:
            thisFileExt = thisFileExt.split('.')[1]
        else:
            thisFileExt = 'null'
        return thisFileExt

    def __logAppend(self, _step):
        '''
        Appends given _step to object attribute self.__log if activateLog is set to True
        :param _step: String describing status on specific event.
        :type _step: string
        '''
        if self.activateLog:
            self.__log.append(_step)

    def __str__(self):
        output = ""
        for each in self.__log:
            output += "--> " + each + "\n"
        return output

    # --------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------

    @property
    def statusDict(self):
        return self.__statusDict

    @statusDict.setter
    def statusDict(self, d):
        self.__statusDict = d

    @property
    def forceOverwrite(self):
        return self.__forceOverwrite

    @forceOverwrite.setter
    def forceOverwrite(self, f):
        self.__forceOverwrite = f

    @property
    def log(self):
        return self.__log

    @property
    def activateLog(self):
        return self.__activateLog

    @activateLog.setter
    def activateLog(self, a):
        self.__activateLog = a


# --------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------

def main():
    pass


if __name__ == "__main__":
    main()
