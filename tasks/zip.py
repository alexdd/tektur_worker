#    Tektur Worker - Camuda external task executor for ETL processes 
#    Copyright (C) 2020  Alex Duesel, tekturcms@gmail.com

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, zipfile
from errors import TaskError

def zipper(dirPath=None, zipFilePath=None, includeDirInZip=True):

    parentDir, dirToZip = os.path.split(dirPath)
    
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return archivePath
    
    outFile = zipfile.ZipFile(zipFilePath, "w",
        compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            outFile.writestr(zipInfo, "")
    outFile.close()
    
def unzipper(file, path):

    unzip = zipfile.ZipFile(file)
    unzip.extractall(path=path)
    
def file_zip(process_dir, variables):
    
    """This task zips the files referenced by their filname.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["inputFolder"] -- The folder to be zipped
        ["zipFilename"] -- Filename of the ZIP file
        ["includeDir"] -- boolean flag if the parent dir should be included
    """
    
    try:
        zipper(os.path.join(process_dir, variables["inputFolder"]["value"]), 
               os.path.join(process_dir, variables["zipFilename"]["value"]),
               variables["includeDir"]["value"] == 'True')
    except Exception as e:
        raise TaskError("ZIP Error!", str(e))
    return {}

def file_unzip(process_dir, variables):

    """This task unzips the ZIP file referenced by its filname.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictionary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["zipFilename"] -- Filename of the ZIP file to be extracted
        ["outputFolder"] -- Name of the folder to extract the files to
    """
    
    filename = variables["zipFilename"]["value"]
    if not filename:
        raise TaskError("ZIP Error! Filename required")

    try:
        unzipper(os.path.join(process_dir, filename),
                 os.path.join(process_dir, variables["outputFolder"]["value"]))
    except Exception as e:
        raise TaskError("UNZIP Error!",str(e) )
    return {}
