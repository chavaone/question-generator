
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name='question-generator',
    version='0.1.0',
    description='Python Random Question Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Marcos Chavarría Teijeiro',
    author_email='chavarria1991@gmail.com',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='maths question moodle',  # Optional

    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required

    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',

    install_requires=[
        'mpmath==1.3.0',
        'sympy==1.5.1'
        ],

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/chavaone/question-generator/issues',
        'Source': 'https://github.com/chavaone/question-generator',
    },
)
