"""
This is the SiteSim Python package. SiteSim is a
"""

import os
import importlib
import logging

# try to import Dulwich or create dummies
try:
    from dulwich.contrib.release_robot import get_current_version
    from dulwich.repo import NotGitRepository
except ImportError:
    NotGitRepository = NotImplementedError

    def get_current_version(*args, **kwargs):
        raise NotGitRepository

# Dulwich Release Robot
BASEDIR = os.path.dirname(__file__)  # this directory
PROJDIR = os.path.dirname(BASEDIR)
VER_FILE = 'version'  # name of file to store version
# use release robot to try to get current Git tag
try:
    GIT_TAG = get_current_version(PROJDIR)
except NotGitRepository:
    GIT_TAG = None
# check version file
try:
    version = importlib.import_module('%s.%s' % (__name__, VER_FILE))
except ImportError:
    VERSION = None
else:
    VERSION = version.VERSION
# update version file if it differs from Git tag
if GIT_TAG is not None and VERSION != GIT_TAG:
    with open(os.path.join(BASEDIR, VER_FILE + '.py'), 'w') as vf:
        vf.write('VERSION = "%s"\n' % GIT_TAG)
else:
    GIT_TAG = VERSION  # if Git tag is none use version file
VERSION = GIT_TAG  # version

LOGGER = logging.getLogger(__name__)  # get logger named for this module
LOGGER.setLevel(logging.DEBUG)  # set logger level to debug
LOGGER.propagate = False  # do not propagate Django logger
CH = logging.StreamHandler()  # create console handler
CH.setLevel(logging.DEBUG)  # set handler level to debug
# create formatter
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = ('\n[%(levelname)s/%(name)s:%(lineno)d] %(asctime)s ' +
              '(%(processName)s/%(threadName)s)\n> %(message)s')
FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)
CH.setFormatter(FORMATTER)  # add formatter to ch
LOGGER.addHandler(CH)  # add console handler to logger

PKG_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_PATH = os.path.dirname(PKG_PATH)

__author__ = 'Bart Wiktorowicz'
__email__ = u'bart.wiktorowicz@sunpowercorp.com'
__url__ = u'https://github.com/SunPower/site_sim'
__version__ = VERSION
__release__ = 'Apollo'
