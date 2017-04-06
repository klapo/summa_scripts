import os
import re
import sys
import warnings
try:
	from setuptools import setup
	from setuptools.extension import Extension
except:
	from distutils.core import setup
	from distutils.extension import Extension

setup(name='summa_scripts',
	author="Nic Wayand and Karl Lapo",
	author_email="lapok@atmos.washington.edu",
	description="Python scripts for managing summa model runs",
	version='0.1',
	packages=["settings"])
