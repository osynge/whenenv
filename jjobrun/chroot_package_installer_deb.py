import logging
import watcher

import time
import json
import datetime
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
import chroot_package_installer_base

syncDelay = datetime.timedelta(seconds=100)
timeoutDelay = datetime.timedelta(seconds=500)
syncDelayShort = datetime.timedelta(seconds=1)
timeoutDelayShort = datetime.timedelta(seconds=5)

class ChrootPackageInstallerDebian2(chroot_package_installer_base.ChrootPackageInstallerBase):

    def __init__(self, *args, **kwargs):
        chroot_package_installer_base.ChrootPackageInstallerBase.__init__(self,args, kwargs)
        # we still need these things chrootCmd, env):
        self.log = logging.getLogger("ChrootPackageInstallerDebian2")
        self.cmdInstallPackage = "apt-get install -y "
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
                
            #self.logOutput(fd,data,args,keys)
            
    def logOutputPkgCatUpdate(self,fd,data,args,keys):
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
            if self.waitingOnPromptPkgCatUpdateStart == True:
                matches = self.promptPkgCatUpdateStart.match(line)
                if matches != None:
                    self.waitingOnPromptPkgCatUpdateStart = False
                    self.waitingOnPromptPkgCatUpdateEnd = True
                    continue
            if not cleanline[:15] == '{ "Package" : "':
               continue
            fred = json.loads(cleanline)
            
            if fred["Status"] ==  'install ok installed':
                if fred["Package"] == "rpm":
                    print "adding rpm",fred["Status"]
                foundpackages.add(str(fred["Package"]))
                continue
            if fred["Status"] ==  u'deinstall ok config-files':
                deinstalledPackages.add(str(fred["Package"]))
                continue
            #print fred
            self.logOutput(fd,data,args,keys)
        
        missing = foundpackages.difference(self.PkgCatInstalled)
        for item in missing:
            self.PkgCatInstalled.add(item)
        missing = deinstalledPackages.difference(self.PkgCatInstalled)
        for item in missing:
            self.PkgCatDeinstall.add(item)
        
        
        return True
    def logOutputPkginstall(self,fd,data,args,keys):
        #self.log.info("logOutputPkginstall")
        Now = datetime.datetime.now()
        self.SyncTime = syncDelay + Now
        self.logOutput(fd,data,args,keys)
        lines = data.split('\n')
        foundpackages = set([])
        deinstalledPackages = set([])
        for line in lines:
            cleanline = line.strip()
            if len(cleanline) == 0:
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
        
        
        

        
    def updatePackages(self):
        Now = datetime.datetime.now()
        self.SyncTime = syncDelay + Now
        TimeOutTime = timeoutDelay + Now
        self.waitingOnPromptPkgCatUpdateEnd = False
        
        self.waitingOnPromptPkgCatUpdateStart = True
        self.PkgCatInstalled = set([])
        #self.shell.Write("apt-get update -y\n")
        cmd = "/usr/bin/dpkg-query -W -f '{ \"Package\" : \"${Package}\", \"Status\" : \"${Status}\" }\n'"
        self.running.CbAddOnFdRead(self.logOutputPkgCatUpdate)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        
        self.promptPkgCatUpdateStart = re.compile(startPrompt)
        self.promptPkgCatUpdateEnd = re.compile(endPrompt)
        
        self.running.Write("echo %s\n" % (startPrompt))
        
        while self.promptPkgCatUpdateStart == True:
            self.running.Comunicate(timeout = 1)
            Now = datetime.datetime.now()
            if Now > self.SyncTime:
                self.log.error("echo sync")
                self.running.Write("echo %s\n" % (startPrompt))
                self.SyncTime = syncDelay + Now
            if Now > TimeOutTime:
                self.log.error("updatePackages time out 1")
                break
        self.SyncTime = syncDelay + Now
        TimeOutTime = timeoutDelay + Now
        self.running.Write("%s\n" % (cmd))
        self.waitingOnPromptPkgCatUpdateEnd = True
        counter = 0
        self.running.Write("echo %s\n" % (endPrompt))
        while self.waitingOnPromptPkgCatUpdateEnd == True:
            self.running.Comunicate(timeout = 1)
            Now = datetime.datetime.now()
            if Now > self.SyncTime:
                self.log.error("echo sync")
                self.running.Write("echo %s\n" % (endPrompt))
                self.SyncTime = syncDelay + Now
                
            if Now > TimeOutTime:
                self.log.error("updatePackages time out 2")
                break
        self.running.CbDelOnFdRead(self.logOutputPkgCatUpdate)
        return self.PkgCatInstalled
    
