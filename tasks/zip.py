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

    try:
        zipper(os.path.join(process_dir, variables["inputFilenames"]["value"]), 
               os.path.join(process_dir, variables["zipFilename"]["value"]))
    except Exception as e:
        raise TaskError("ZIP Error!", str(e))

def file_unzip(process_dir, variables):

    try:
        unzipper(os.path.join(process_dir, variables["zipFilename"]["value"]),
                 os.path.join(process_dir, variables["outputFolder"]["value"]))
    except Exception as e:
        raise TaskError("UNZIP Error!",str(e) )
