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
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("uploaderFacade")
        self._packageInstallerImp = None
        self.packaging = kwargs.get('packaging', None)
        self.chrootCmd = kwargs.get('command', None)
        self.chrootEnv = kwargs.get('enviroment', None)
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
                        return self._packageInstallerImp.chrootPath
                    else:
                        return None
            return self._chrootPath

        def fset(self, path):
            self._chrootPath = path
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    self._packageInstallerImp.chrootPath = path
        def fdel(self):
            del self._chrootPath
        return locals()

    @Property
    def chrootCmd():
        doc = "The person's name"

        def fget(self):
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    if hasattr(self._packageInstallerImp,'chrootCmd'):
                        return self._packageInstallerImp.chrootCmd
                    else:
                        return None
            return self._chrootCmd

        def fset(self, cmd):
            self._chrootCmd = cmd
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    self._packageInstallerImp.chrootCmd = cmd
        def fdel(self):
            del self._chrootCmd
        return locals()

    @Property
    def chrootEnv():
        doc = "The person's name"

        def fget(self):
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    if hasattr(self._packageInstallerImp,'chrootEnv'):
                        return self._packageInstallerImp.chrootEnv
                    else:
                        return None
            return self._chrootEnv

        def fset(self, env):
            self._chrootEnv = env
            if hasattr(self, '_packageInstallerImp'):
                if self._packageInstallerImp != None:
                    self._packageInstallerImp.chrootEnv = env
        def fdel(self):
            del self._chrootEnv
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
                self._packageInstallerImp.chrootEnv = self.chrootEnv
                self._packageInstallerImp.chrootCmd = self.chrootCmd
                self._packageInstallerImp.chrootPath = self.chrootPath

        def fdel(self):
            del self._uploader
        return locals()

    def installPackages(self,packages):
        if hasattr(self, '_packageInstallerImp'):
            remotepath = self.transforExtUri(externalURI)
            return self._packageInstallerImp.installPackages(packages)
        else:
            self.log.error("No implementation")
    def initialise(self):
        if hasattr(self, '_packageInstallerImp'):
            return self._packageInstallerImp.initialise()
        else:
            self.log.error("No implementation")
    def updatePackages(self):
        if hasattr(self, '_packageInstallerImp'):
            return self._packageInstallerImp.updatePackages()
        else:
            self.log.error("No implementation")
def tester_owen():
    obj2test = ChrootPackageInstallerRedhat()
    print updatePackages

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tester_owen()

