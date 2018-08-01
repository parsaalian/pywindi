from setuptools import setup, find_packages

print(find_packages())

setup(name='pywindi',
    version='1.3.0',
    description='Wrapper for pyindi',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords='pyindi pyindi-client camera',
    url='https://gitlab.com/parsaalian0/windi',
    authors='Parsa Alian & Emad Salehi',
    author_email='emad.s1178@yahoo.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        capture=pywindi.scripts.capture:cli
    ''',
    zip_safe=False)
