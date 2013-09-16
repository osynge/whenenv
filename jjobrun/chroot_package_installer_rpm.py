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

class ChrootPackageInstallerRedhat(chroot_package_installer_base.ChrootPackageInstallerBase):

    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        chroot_package_installer_base.ChrootPackageInstallerBase.__init__(self,args, kwargs)
        self.log = logging.getLogger("ChrootPackageInstallerRedhat")
        self.cmdInstallPackage = "yum install -y -q"
        
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
        self.log.error("logOutputPkgCatUpdate start")
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
                for item in line.split(','):
                    if len(item) == 0:
                        continue
                    foundpackages.add(item)
            if self.waitingOnPromptPkgCatUpdateStart == True:
                matches = self.promptPkgCatUpdateStart.match(line)
                if matches != None:
                    self.waitingOnPromptPkgCatUpdateStart = False
                    self.waitingOnPromptPkgCatUpdateEnd = True
                    print "hereh"
                    continue
            
            
            #print fred
            #self.logOutput(fd,data,args,keys)
        self.PkgCatInstalled = foundpackages
        self.log.error("logOutputPkgCatUpdate end %s" % (len(foundpackages)))
        return True

    def logOutputPkginstall(self,fd,data,args,keys):    
        self.logOutputPkg(fd,data,args,keys)

        
    def updatePackages(self):
        
        rc = self.running.returncode()
        self.log.error("rc=%s" % (rc))
        Now = datetime.datetime.now()
        self.SyncTime = syncDelay + Now
        TimeOutTime = timeoutDelay + Now
        self.waitingOnPromptPkgCatUpdateEnd = False
        
        self.waitingOnPromptPkgCatUpdateStart = True
        self.PkgCatInstalled = set([])
        #self.shell.Write("apt-get update -y\n")
        cmd = '\nrpm -qa --qf ",%{NAME}"\n'
        #cmd = "\necho\n"
        self.running.CbAddOnFdRead(self.logOutputPkgCatUpdate)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.running.CbAddOnFdRead(self.logOutput)
        self.promptPkgCatUpdateStart = re.compile(startPrompt)
        self.promptPkgCatUpdateEnd = re.compile(endPrompt)
        self.log.error("starting lookp one")
        self.running.Write("echo %s\n" % (startPrompt))
        
        while self.promptPkgCatUpdateStart == True:
            self.running.Comunicate(timeout = 1)
            rc = self.running.returncode()
            if rc != None:
                self.log.error("rc=%s" % (rc))
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
        self.running.Write("echo %s\n" % (endPrompt))
        self.waitingOnPromptPkgCatUpdateEnd = True
        self.log.error("starting lookp two")
        self.SyncTime = syncDelayShort + Now
        TimeOutTime = timeoutDelayShort + Now
        while self.waitingOnPromptPkgCatUpdateEnd == True:
            self.running.Comunicate(timeout = 1)
            Now = datetime.datetime.now()
            rc = self.running.returncode()
            if rc != None:
                self.log.error("rc=%s" % (rc))
            if Now > self.SyncTime:
                
                self.log.error("echo sync 44")
                self.running.Write("\necho %s\n" % (endPrompt))
                self.SyncTime = syncDelayShort + Now
                
            if Now > TimeOutTime:
                self.log.error("updatePackages time out 2")
                break
        self.running.CbDelOnFdRead(self.logOutputPkgCatUpdate)
        self.running.CbDelOnFdRead(self.logOutput)
        return self.PkgCatInstalled

 
