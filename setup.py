from distutils.core import setup


setup(
    name='dl_markup',
    version='0.0.1',
    packages=['dl_markup',],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'dl_markup = dl_markup.__main__:main',
        ],
    }
)
