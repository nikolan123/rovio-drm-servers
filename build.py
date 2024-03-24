import subprocess

cmd = [
    'python',
    '-m', 'PyInstaller',
    'main.py',
    '--name', 'Rovio CAS', # name of app
    '--onefile',
    #'--windowed', # prevent console appearing
]
subprocess.call(cmd)
