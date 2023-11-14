from setuptools import setup
import re

_version_re = re.compile(r"(?<=^__version__ = (\"|'))(.+)(?=\"|')")

def get_version(rel_path: str) -> str:
    """
    Searches for the ``__version__ = `` line in a source code file.

    https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    """
    with open(rel_path, 'r') as f:
        matches = map(_version_re.search, f)
        filtered = filter(lambda m: m is not None, matches)
        version = next(filtered, None)
        if version is None:
            raise RuntimeError(f'Could not find __version__ in {rel_path}')
        return version.group(0)


setup(
    name='mni2common',
    version=get_version('mni2common.py'),
    description='A ChRIS plugin to convert MINC volume and MNI .obj surface file formats to NIFTI and MZ3 OBJ respectively.',
    author='FNNDSC',
    author_email='jennings.zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-mni2common',
    py_modules=['mni2common'],
    install_requires=['chris_plugin==0.3.1', 'tqdm~=4.66'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'mni2common = mni2common:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1'
        ]
    }
)
