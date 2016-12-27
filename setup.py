import os
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

"""
New release procedure

- edit pierky/blocklistsaggregator/version.py

- edit CHANGES.rst

- verify RST syntax is ok
    python setup.py --long-description | rst2html.py --strict

- new files to be added to MANIFEST.in?

- python setup.py sdist

- twine upload dist/*

- git push

- edit new release on GitHub
"""

__version__ = None

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get proper long description for package
current_dir = dirname(abspath(__file__))
description = open(join(current_dir, "README.rst")).read()
changes = open(join(current_dir, "CHANGES.rst")).read()
long_description = '\n\n'.join([description, changes])
exec(open(join(current_dir, "pierky/blocklistsaggregator/version.py")).read())

# Get the long description from README.md
setup(
    name="blocklistsaggregator",
    version=__version__,

    packages=["pierky", "pierky.blocklistsaggregator"],
    namespace_packages=["pierky"],
    include_package_data=True,

    license="GPLv3",
    description="A Python tool that downloads IP block lists from various sources and builds configurations for network equipments and firewalls.",
    long_description=long_description,
    url="https://github.com/pierky/blocklistsaggregator",
    download_url="https://github.com/pierky/blocklistsaggregator",

    author="Pier Carlo Chiodi",
    author_email="pierky@pierky.com",
    maintainer="Pier Carlo Chiodi",
    maintainer_email="pierky@pierky.com",

    install_requires=[
        "netaddr",
        "six"
    ],

    scripts=["scripts/blocklistsaggregator"],

    keywords=['Malware', 'Spam', 'BlockList', 'Networking'],

    classifiers=[
        "Development Status :: 4 - Beta",

        "Environment :: Console",

        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: POSIX",
        "Operating System :: Unix",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",

        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Security"
    ],
)
