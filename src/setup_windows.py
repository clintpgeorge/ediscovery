from distutils.core import setup
import py2exe

packages = []
for dbmodule in ['dbhash', 'gdbm', 'dbm', 'dumbdbm','_pybsddb', 'bsddb3.dbutils']:
    try:
        __import__(dbmodule)
    except ImportError:
        pass
    else:
        # If we found the module, ensure it's copied to the build directory.
        packages.append(dbmodule)
setup(
    options = {'py2exe': {'bundle_files': 3, "dll_excludes": ["mswsock.dll", "MSWSOCK.dll"], "packages": packages}},
    zipfile = None,
    windows = [{
            "script": 'gui/RandomSampler.py',
            "icon_resources": [(1, 'gui/res/uflaw.ico')],
            "dest_base":"RandomSampler"
            }],
)
