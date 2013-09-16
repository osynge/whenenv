import logging
import uuid
import base64
import string
import pexpect
import re
import prompts

transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )


import watcher

import time
import json
import datetime

import chroot_package_installer_deb
import chroot_package_installer_rpm


syncDelay = datetime.timedelta(seconds=100)
timeoutDelay = datetime.timedelta(seconds=500)
syncDelayShort = datetime.timedelta(seconds=1)
timeoutDelayShort = datetime.timedelta(seconds=5)

def Property(func):
    return property(**func())

class chrootPackageFacard(object):
    """Facade class for mulitple implementations of uploader,
    Should be robust for setting the impleemntation or attributes
    in any order."""
    def __init__(self):
        self.log = logging.getLogger("uploaderFacade")
        self._packageInstallerImp = None
        self.externalPrefix = None
    def HasImplementation(self):
        if hasattr(self, '_packageInstallerImp'):
            return True
        else:
            return False
    
    @Property
    def chrootPath():
        doc = "The person's name"

        def fget(self):
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    if hasattr(self._packageInstallerImp,'remotePrefix'):
                        return self._packageInstallerImp.remotePrefix
                    else:
                        return None
            return self._remotePrefix

        def fset(self, path):
            self._chrootPath = path
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    self._packageInstallerImp.chrootPath = path
        def fdel(self):
            del self._chrootPath
        return locals()

    @Property
    def packaging():
        doc = """packaging type
        can be rpm or deb"""

        def fget(self):
            return self._uploaderName

        def fset(self, name):
            self._uploader = name
            if name == "rpm":
                self._packageInstallerImp = chroot_package_installer_rpm.ChrootPackageInstallerRedhat()
            elif name == "deb":
                self._packageInstallerImp = chroot_package_installer_deb.ChrootPackageInstallerDebian2()
            else:
                self.log.error("Invalid packagin sellected '%s'" % (name))
                del(self._packageInstallerImp)
            if hasattr(self, '_packageInstallerImp'):
                self._packageInstallerImp.remotePrefix = self.remotePrefix            
            
        def fdel(self):
            del self._uploader
        return locals()

    def installPackages(self,packages):
        if hasattr(self, '_packageInstallerImp'):
            remotepath = self.transforExtUri(externalURI)
            return self._packageInstallerImp.installPackages(packages)

def tester_owen():
    obj2test = ChrootPackageInstallerRedhat()
    print updatePackages

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tester_owen()

