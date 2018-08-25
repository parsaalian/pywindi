from setuptools import setup, find_packages
from pywindi.__init__ import __version__

setup(name='pywindi',
    version=__version__,
    description='Wrapper for pyindi',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords='pyindi pyindi-client indi',
    url='https://gitlab.com/parsaalian0/windi',
    authors='Parsa Alian & Emad Salehi',
    author_email='emad.s1178@yahoo.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        capture=pywindi.scripts.capture:capturer_cli
        ccdconfig=pywindi.scripts.config:config_cli
    ''',
    zip_safe=False)
