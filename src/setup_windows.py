from distutils.core import setup
import py2exe
setup(
    windows = [
        {
            "script": 'gui/RandomSampler.py',
            "icon_resources": [(1, 'gui/res/uflaw-edisc1-icon.ico')]
        }
    ],
)
