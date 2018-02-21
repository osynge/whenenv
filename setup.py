from jjobrun.__version__ import version
from sys import version_info

try:
    from setuptools import setup, find_packages
except ImportError:
	try:
            from distutils.core import setup
	except ImportError:
            from ez_setup import use_setuptools
            use_setuptools()
            from setuptools import setup, find_packages
import os

Application = 'whenenv'

def determine_path ():
    """Borrowed from wxglade.py"""
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print("I'm sorry, but something is wrong.")
        print("There is no __file__ variable. Please contact the author.")
        sys.exit ()

setup_args = {
    "name" : Application,
    "version" : version,
    "description": """whenenv removes branching in shell scripts typical use might be running jenkins matrix builds.""",
    "author" : "O M Synge",
    "author_email" : "owen.synge@desy.de",
    "license" : 'Apache Sytle License (2.0)',
    "install_requires" : [
       "nose >= 1.1.0",
       "pexpect",
        ],
    "test_suite" : 'nose.collector',
    "tests_require" : [
        'coverage >= 3.0',
        'pexpect',
        'mock',
        ],
    "url" : 'https://github.com/osynge/whenenv.git',
    "packages" : ['jjobrun'],
    "classifiers" : [
        'Development Status :: 1 - UnStable',
        'Environment :: GUI',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],
    "scripts" : ['whenenv','jenkinsjobrunner'],
}

needs_scripts = True
needs_jobs = True
needs_docs = True

if "VIRTUAL_ENV" in os.environ:
    needs_scripts = False
    needs_jobs = False
    needs_docs = False

if "WITHOUT_DOC" in os.environ:
    needs_docs = False

if needs_jobs or needs_scripts or needs_docs:
    data_files = []
    path = determine_path ()
    if needs_scripts is True:
        scriptsPath = os.environ.get("SCRIPT_DIR")
        if scriptsPath is None:
            scriptsPath = "%s/%s" % (path,"/transfer/")
        installdir_scripts = '/usr/share/lib/%s/scripts' % (Application)
        scriptsIncludeList = []
        for script in os.listdir(scriptsPath):
            newPath = "%s/%s" % (scriptsPath,script)
            scriptsIncludeList.append(newPath)
        if len(scriptsIncludeList) > 0:
            data_files.append((installdir_scripts, scriptsIncludeList))
    if needs_jobs is True:
        jobsPath = os.environ.get("JOB_DIR")
        if jobsPath is None:
            jobsPath = "%s/%s" % (path,"/jobs/")
        installdir_jobs = '/usr/share/lib/%s/jobs' % (Application)
        jobsIncludeList = []
        for job in os.listdir(jobsPath):
            newPath = "%s/%s" % (jobsPath,job)
            jobsIncludeList.append(newPath)
        if len(jobsIncludeList) > 0:
            data_files.append((installdir_jobs, jobsIncludeList))
    if needs_docs is True:
        installdir_doc = "/usr/share/doc/%s-%s" % (Application,version)
        data_files.append((installdir_doc,['README.md','LICENSE','ChangeLog']))
    setup_args["data_files"] = data_files

setup(**setup_args)
