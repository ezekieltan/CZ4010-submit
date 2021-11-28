import os
class FileSystemUtilities:
    __instance__ = None
    def __init__(self):
        if FileSystemUtilities.__instance__ is None:
            FileSystemUtilities.__instance__ = self
        else:
            pass
    @staticmethod
    def getInstance():
        if not FileSystemUtilities.__instance__:
            FileSystemUtilities()
        return FileSystemUtilities.__instance__
    
    @staticmethod
    def removeExtension(path):
        return os.path.splitext(path)[0]
    @staticmethod
    def getSubfolders(folder):
        return [ os.path.basename(os.path.normpath(f.path)) for f in os.scandir(folder) if f.is_dir() ]
    @staticmethod
    def getFilesInFolder(folder, extensions = True):
        ret = [ os.path.basename(os.path.normpath(f.path)) for f in os.scandir(folder) if not f.is_dir() ]
        if extensions == False:
            ret = [FileSystemUtilities.removeExtension(f) for f in ret]
        return ret
    @staticmethod
    def dir(directory, files = True, folders = True, extensions = True):
        ret = []
        if(files):
            ret = ret + FileSystemUtilities.getFilesInFolder(directory, extensions = extensions)
        if(folders):
            ret = ret + FileSystemUtilities.getSubfolders(directory)
        return ret
    @staticmethod
    def createFolder(path):
        os.makedirs(path, exist_ok=True)