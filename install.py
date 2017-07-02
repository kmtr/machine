import pip

_all_ = [
    "python-osc>=1.6.3",
]

windows = []

linux = [
    "pigpio>=1.35",
]

darwin = []

def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':

    from sys import platform

    install(_all_) 
    if platform == 'windows':
        install(windows)
    if platform.startswith('linux'):
        install(linux)
    if platform == 'darwin': # MacOS
        install(darwin)