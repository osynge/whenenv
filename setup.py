from sqtray.__version__ import version
from sys import version_info

from distutils.core import setup

Application = 'whenenv'

setup(name=Application,
    version=version,
    description="whenenv removes branching in shell scripts typical use might be running jenkins matrix builds.""",
    author="O M Synge",
    author_email="owen.synge@desy.de",
    license='Apache Sytle License (2.0)',
    install_requires=[
       "bash",
        ],
    url = 'https://github.com/hepix-virtualisation/hepixvmilsubscriber',
    packages = ['sqtray'],
    classifiers=[
        'Development Status :: 1 - UnStable',
        'Environment :: GUI',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],
    scripts=['squeezetray'],
    data_files=[('/usr/share/doc/%s-%s' % (Application,version),['README','LICENSE','ChangeLog'])]    
)
