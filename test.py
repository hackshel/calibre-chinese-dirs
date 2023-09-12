import zipfile
import pprint

zipfilename = 'pylib3.zip'

zf = zipfile.ZipFile(zipfilename)

infos = zf.infolist()

for  info in infos:
   print(info.filename)



