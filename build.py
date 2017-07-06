from cx_Freeze import setup, Executable

executables = [Executable('main.py',
                          targetName='Feven.exe',
                          base='Win32GUI',
                          icon="feven.ico")]

excludes = ['unittest', 'email', 'html', 'http', 'urllib', 'xml',
            'unicodedata', 'bz2', 'select', 'pydoc_data']

zip_include_packages = ['collections', 'encodings', 'importlib', 'wx',
                        'logging', 'ctypes', 'pathtools']

include_files = ['feven.ico', 'presets']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,
    }
}

setup(name='Feven',
      version='0.0.1',
      description='Fuzzy Eve Notifier',
      executables=executables,
      options=options)
