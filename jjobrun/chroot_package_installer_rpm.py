import logging

import time
import json
import datetime
import logging
import uuid
import base64
import string
import pexpect
import re

import sys


from . import watcher
from . import prompts

import time
import json
import datetime

from . import chroot_package_installer_base

transtbl = None
if sys.version_info < (3,):
    transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )

if sys.version_info > (3,):
    transtbl = str.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )


syncDelay = datetime.timedelta(seconds=100)
timeoutDelay = datetime.timedelta(seconds=500)
syncDelayShort = datetime.timedelta(seconds=1)
timeoutDelayShort = datetime.timedelta(seconds=5)

class ChrootPackageInstallerRedhat(chroot_package_installer_base.ChrootPackageInstallerBase):

    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        chroot_package_installer_base.ChrootPackageInstallerBase.__init__(self,args, kwargs)
        self.log = logging.getLogger("ChrootPackageInstallerRedhat")
        self.cmdUpdatePackageList = "yum update"
        self.cmdInstallPackage = "yum install -y -q"
        #self.cmdQueryPackageInstalled = 'rpm -qa --qf ",%{NAME}"'
        self.cmdQueryPackageInstalled = """rpm -qa --qf '\{ "Package" : "%{NAME}", "Vendor" : "%{VENDOR}" \}\n'"""
        
    def logOutputPkg(self,fd,data,args,keys):
        lines = data.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            if self.waitingOnPromptPkgInstallEnd == True:
                matches = self.promptPkgInstallEnd.match(line)
                if matches != None:
                    self.waitingOnPromptPkgInstallEnd = False
                    continue
            if self.waitingOnPromptPkgInstallStart == True:
                matches = self.promptPkgInstallStart.match(line)
                if matches != None:
                    self.waitingOnPromptPkgInstallStart = False
                    self.waitingOnPromptPkgInstallEnd = True
                    continue
                
            self.logOutput(fd,data,args,keys)
            
    def logOutputPkgCatUpdate(self,fd,data,args,keys):
        self.log.debug("logOutputPkgCatUpdate start")
        lines = data.split('\n')
        foundpackages = set([])
        deinstalledPackages = set([])
        for line in lines:
            cleanline = line.strip()
            if len(cleanline) == 0:
                continue
            if self.waitingOnPromptPkgCatUpdateEnd == True:
                matches = self.promptPkgCatUpdateEnd.match(line)
                if matches != None:
                    self.waitingOnPromptPkgCatUpdateEnd = False
                    continue
                #for item in line.split(','):
                #    if len(item) == 0:
                #        continue
                #    foundpackages.add(item)
            if self.waitingOnPromptPkgCatUpdateStart == True:
                matches = self.promptPkgCatUpdateStart.match(line)
                if matches != None:
                    self.waitingOnPromptPkgCatUpdateStart = False
                    self.waitingOnPromptPkgCatUpdateEnd = True
                    continue
            if not cleanline[:15] == '{ "Package" : "':
               continue
            fred = json.loads(cleanline)
            foundpackages.add(str(fred["Package"]))
            #print fred
            #self.logOutput(fd,data,args,keys)
        self.PkgCatInstalled = foundpackages
        self.log.debug("logOutputPkgCatUpdate end len(foundpackages)=%s" % (len(foundpackages)))
        return True

    def logOutputPkginstall(self,fd,data,args,keys):    
        self.logOutputPkg(fd,data,args,keys)

 
