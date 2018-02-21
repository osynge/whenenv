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
import time
import json
import datetime
import sys
from . import watcher
from . import prompts

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

class ChrootPackageInstallerBase(object):

    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        self.log = logging.getLogger("ChrootPackageInstallerBase")
        self.chrootCmd = kwargs.get('command', None)
        self.logOut = logging.getLogger("pkg.out")
        self.logErr = logging.getLogger("pkg.err")
        self.cmdInstallPackage = None

    def logOutput(self,fd,data,args,keys):
        log = self.log
        if fd == 0:
            log = self.logOut
        if fd == 1:
            log = self.logErr
        for line in data.split('\n'):
            cleanline = line.strip()
            if len(cleanline) > 0:
                log.info(cleanline)

    def initialise(self):
        if self.chrootCmd == None:
            self.log.error("No chroot command set")
            return False
        self.running = watcher.LogRunShell(command=self.chrootCmd)
        self.running.Start()
        self.running.Write("set -x \n")
        self.running.Write("set -e \n")
        

        
        
    def finalise(self):
        self.waitingOnExit = (self.running.returncode == None)
        while self.waitingOnExit == True:
            self.log.error("Waiting for exit.")
            time.sleep(1)
            if self.running.returncode != None:
                    self.waitingOnExit = False
            self.running.Write("\nexit 0\n")
            
    
    def installPackages(self,packages):
        notinstalled = set([])
        insalledPkg = self.updatePackages()
        for pack in packages:
            if pack in insalledPkg:
                print (pack, pack in insalledPkg)
                continue
            notinstalled.add(pack)
        
        extra = insalledPkg.difference(packages)
        
        missing = set(packages).difference(insalledPkg)
        self.log.info("notinstalled %s" %(notinstalled))
        self.log.info("extra %s" %(extra))
        for pack in missing:
            self.installPackage(pack)
        insalledPkg = self.updatePackages()
        missing = set(packages).difference(insalledPkg)
        for pack in missing:
            self.installPackage(pack)

    def installPackage(self,package):
        self.log.info("PkgInstall start")
        rc = self.running.returncode()
        if rc != None:
            self.log.info("Package install shell stopped")
            self.initialise()
        if self.cmdInstallPackage == None:
            self.log.error("programing error")
        Now = datetime.datetime.now()
        self.SyncTime = syncDelay + Now
        TimeOutTime = timeoutDelay + Now
        self.waitingOnPromptPkgInstallStart = True
        self.waitingOnPromptPkgInstallEnd = False
        passenv_ignored = set(["PATH","SHLVL","OLDPWD","PS1"])
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptPkgInstallStart = re.compile(startPrompt)
        self.promptPkgInstallEnd = re.compile(endPrompt)
        self.log.debug("promptPkgInstallStart %s" %(startPrompt))
        self.log.debug("promptPkgInstallEnd %s" %(endPrompt))
        self.running.CbAddOnFdRead(self.logOutputPkginstall)
        self.running.Write("echo %s\n" % (startPrompt))
        while self.waitingOnPromptPkgInstallStart == True:
            rc = self.running.returncode()
            if rc != None:
                self.log.error("rc=%s" % (rc))
                break
            self.running.Comunicate(timeout = 1)
            Now = datetime.datetime.now()
            if Now > self.SyncTime:
                self.log.error("echo sync")
                self.running.Write("echo %s\n" % (startPrompt))
                self.SyncTime = syncDelay + Now
            if Now > TimeOutTime:
                self.log.error("installPackage time out 1")
                break
        # we have now synced 
        
        self.waitingOnPromptPkgInstallStart = False
        self.waitingOnPromptPkgInstallEnd = True
        cmd = '%s %s\n' % (self.cmdInstallPackage,package)
        self.running.Write(cmd)
        self.log.info("PkgInstall %s" %(cmd.strip()))
        self.running.Comunicate(timeout = 1)
        self.running.Write("echo %s\n" % (endPrompt))
        Now = datetime.datetime.now()
        self.SyncTime = syncDelay + Now
        TimeOutTime = timeoutDelay + Now
        while self.waitingOnPromptPkgInstallEnd == True:
            rc = self.running.returncode()
            if rc != None:
                self.log.error("rc=%s" % (rc))
                break
            self.running.Comunicate(timeout = 1)
            if Now > self.SyncTime:
                self.log.error("echo sync")
                self.running.Write("echo %s\n" % (endPrompt))
                self.SyncTime = syncDelay + Now
            if Now > TimeOutTime:
                self.log.error("installPackage time out 2")
                break
        self.log.info("checking loop finished %s" %(cmd.strip()))
        self.running.CbDelOnFdRead(self.logOutputPkginstall)
        self.log.info("PkgInstall finished")
        return True
    
    
 
    
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
        cmd = "%s\n" % (self.cmdQueryPackageInstalled)
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
                break
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
                break
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

