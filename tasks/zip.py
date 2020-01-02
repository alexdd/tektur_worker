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
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["inputFilenames"] -- Space separated list of input filenames
        ["zipFilename"] -- Filename of the ZIP file
    """

    try:
        zipper(os.path.join(process_dir, variables["inputFilenames"]["value"]), 
               os.path.join(process_dir, variables["zipFilename"]["value"]))
    except Exception as e:
        raise TaskError("ZIP Error!", str(e))

def file_unzip(process_dir, variables):

    """This task unzips the ZIP file referenced by its filname.

    Attributes:
        process_dir -- the generated working directory of the calling process
        variables -- a dictonary containing key-value pairs passed from Camunda
    Camunda Parameters:
        ["zipFilename"] -- Filename of the ZIP file to be extracted
        ["outputFolder"] -- Name of the folder to extract the files to
    """

    try:
        unzipper(os.path.join(process_dir, variables["zipFilename"]["value"]),
                 os.path.join(process_dir, variables["outputFolder"]["value"]))
    except Exception as e:
        raise TaskError("UNZIP Error!",str(e) )
