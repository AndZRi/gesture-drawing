from Resources import AbsolutePaths

import PyInstaller.__main__

args = [
    'main.py',
    '--name=Anzigos Gesture Drawing',
    '--noconsole',
    '--add-data=data:./data'
]

PyInstaller.__main__.run(args)
PyInstaller.__main__.run(args + ['--onefile'])
