from jjobrun.__version__ import version
from sys import version_info
try:
    from setuptools import setup
except:
    from distutils.core import setup
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
        print "I'm sorry, but something is wrong."
        print "There is no __file__ variable. Please contact the author."
        sys.exit ()

jobsIncludeList = []
scriptsIncludeList = []
path = determine_path ()
jobsPath = "%s/%s" % (path,"/jobs/")
for job in os.listdir(jobsPath):
    newPath = "%s/%s" % (jobsPath,job)
    jobsIncludeList.append(newPath)
scriptsPath = "%s/%s" % (path,"/transfer/")
for job in os.listdir(scriptsPath):
    newPath = "%s/%s" % (scriptsPath,job)
    scriptsIncludeList.append(newPath)

setup(name=Application,
    version=version,
    description="whenenv removes branching in shell scripts typical use might be running jenkins matrix builds.""",
    author="O M Synge",
    author_email="owen.synge@desy.de",
    license='Apache Sytle License (2.0)',
    install_requires=[
       "nose >= 1.1.0",
        ],
    test_suite = 'nose.collector',
    url = 'https://github.com/hepix-virtualisation/hepixvmilsubscriber',
    packages = ['jjobrun'],
    classifiers=[
        'Development Status :: 1 - UnStable',
        'Environment :: GUI',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],
    scripts=['whenenv','jenkinsjobrunner'],
    data_files=[('/usr/share/doc/%s-%s' % (Application,version),['README','LICENSE','ChangeLog']),
        ('/usr/share/lib/%s/jobs' % (Application),jobsIncludeList),
        ('/usr/share/lib/%s/scripts' % (Application),scriptsIncludeList),
        ]    
)
