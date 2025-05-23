from Resources import RelativePaths

import PyInstaller.__main__

args = [
    'main.py',
    '--name=Anzigos Gesture Drawing',
    '--noconsole',
    *[f'--add-data={getattr(RelativePaths, i)}:./{getattr(RelativePaths, i)}' for i in dir(RelativePaths) if not i.startswith('__')]
]

PyInstaller.__main__.run(args)
PyInstaller.__main__.run(args + ['--onefile'])
