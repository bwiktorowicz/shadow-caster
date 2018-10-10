"""
Install Shadow_Caster
"""
import os

try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup
#         from src import __version__

#         BASEDIR = os.path.dirname(__file__)
#         with open(os.path.join(BASEDIR, 'requirements.txt')) as f:
#                 INST_REQ = list(f)  # f.readlines()

setup(name='shadow_caster')
