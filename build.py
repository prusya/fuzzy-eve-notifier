
from cx_Freeze import setup, Executable

executables = [Executable('main.py',
                          targetName='Feven.exe',
                          base='Win32GUI')]

excludes = ['unittest', 'email', 'html', 'http', 'urllib', 'xml',
            'unicodedata', 'bz2', 'select']

zip_include_packages = ['collections', 'encodings', 'importlib', 'wx',
                        'logging', 'watchdog', 'ctypes', 'pathtools']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
    }
}

setup(name='hello_world',
      version='0.0.14',
      description='My Hello World App!',
      executables=executables,
      options=options)