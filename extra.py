import zipfile
import pprint
import os
import os.path

def extraZip(zipFileName, targetPath):

    zf = zipfile.ZipFile(zipFileName)
    filelist = zf.namelist()

    for f in filelist:
        pprint.pprint(f)
        info = zf.getinfo(f)
        if info.file_size == 0:
    	    path = os.path.join(targetPath,info.filename)
            os.makedirs(path)
        else:
    	    zf.extract(f, targetPath)

    zf.close()

if __name__ == '__main__':

    zipFileName = 'pylib.zip'
    targetPath = 'pylib'


    extraZip(zipFileName, targetPath)
