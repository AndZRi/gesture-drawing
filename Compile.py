from modules.Resources import RelativePaths

import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=Anzigos Gesture Drawing',
    '--onefile',
    '--noconsole',
    *[f'--add-data={getattr(RelativePaths, i)}:./{getattr(RelativePaths, i)}' for i in dir(RelativePaths) if not i.startswith('__')]
])
