import zipfile
import os
import os.path


class Env(object):

    def __init__(self, build_dir):
        self.app_base = os.path.abspath(build_dir)
        self.lib_dir = os.path.join(self.app_base, 'pylib')
        self.pylib = os.path.join(self.app_base, 'pylib2.zip')
        self.dll_dir = os.path.join(self.app_base, 'DLLs')



def zipDir(dirPath, zipFileName):

    zf = zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_STORED)
    
    for path, dirnames, filenames in os.walk(dirPath):
        fpath = path.replace(dirPath, '')

        for filename in filenames:
            zf.write(os.path.join(path, filename), os.path.join(fpath, filename))

    zf.close()

def add_to_zipfile(zf, name, base, zf_names):
    abspath = os.path.join(base, name)
    name = name.replace(os.sep, '/')
    if name in zf_names:
        raise ValueError('Already added %r to zipfile [%r]' % (name, abspath))
    zinfo = zipfile.ZipInfo(filename=name, date_time=(1980, 1, 1, 0, 0, 0))

    if os.path.isdir(abspath):
        if not os.listdir(abspath):
            return
        zinfo.external_attr = 0o700 << 16
        zf.writestr(zinfo, '')
        for x in os.listdir(abspath):
            add_to_zipfile(zf, name + os.sep + x, base, zf_names)
    else:
        ext = os.path.splitext(name)[1].lower()
        if ext in ('.dll',):
            raise ValueError('Cannot add %r to zipfile' % abspath)
        zinfo.external_attr = 0o600 << 16
        if ext in ('.py', '.pyc', '.pyo'):
            with open(abspath, 'rb') as f:
                zf.writestr(zinfo, f.read())

    zf_names.add(name)



def archive_lib_dir(env):
    print('Putting all python code into a zip file for performance')
    zf_names = set()
    with zipfile.ZipFile(env.pylib, 'w', zipfile.ZIP_STORED) as zf:
        # Add everything in Lib except site-packages to the zip file
        listdirs = os.listdir(env.lib_dir)
        for x in listdirs.sort(key=lambda x:int(x[4:-4])):
            if x == 'site-packages':
                continue
            add_to_zipfile(zf, x, env.lib_dir, zf_names)

	"""
        sp = os.path.join(env.lib_dir, 'site-packages')
        # Special handling for pywin32
        handled = {'pywin32.pth', 'win32'}
        base = os.path.join(sp, 'win32', 'lib')
        for x in os.listdir(base):
            if os.path.splitext(x)[1] not in ('.exe',):
                add_to_zipfile(zf, x, base, zf_names)
        base = os.path.dirname(base)
        for x in os.listdir(base):
            if not os.path.isdir(os.path.join(base, x)):
                if os.path.splitext(x)[1] not in ('.exe',):
                    add_to_zipfile(zf, x, base, zf_names)

        # We dont want the site.py (if any) from site-packages
        handled.add('site.pyo')

        # The rest of site-packages
        for x in os.listdir(sp):
            if x in handled or x.endswith('.egg-info'):
                continue
            absp = os.path.join(sp, x)
            if os.path.isdir(absp):
                if not os.listdir(absp):
                    continue
                add_to_zipfile(zf, x, sp, zf_names)
            else:
                add_to_zipfile(zf, x, sp, zf_names)


	"""



if __name__ ==  '__main__':


    dirPath = 'pylib'
    zipFileName = 'pylib2.zip'

    env = Env('./')
    env.pylib = 'pylib3.zip'
    print(env)

    archive_lib_dir(env)
    #zipDir(dirPath, zipFileName)

  

