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


class ChrootPackageInstallerDebian2(object):

    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        self.log = logging.getLogger("ChrootPackageInstallerDebian2")
        self.chrootCmd = kwargs.get('command', None)
        self.logOut = logging.getLogger("pkg.out")
        self.logErr = logging.getLogger("pkg.err")
        
    
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
        pass
    def initialise(self):
        if self.chrootCmd == None:
            self.log.error("No chroot command set")
            return False
        self.running = watcher.LogRunShell(command=self.chrootCmd)
        self.running.Start()
        self.running.Write("set -x \n")
        self.running.Write("set -e \n")
        
    def updatePackages(self):
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
        self.running.Write("%s\n" % (cmd))
        self.waitingOnPromptPkgCatUpdateEnd = True
        counter = 0
        self.running.Write("echo %s\n" % (endPrompt))
        while self.waitingOnPromptPkgCatUpdateEnd == True:
            self.running.Comunicate(timeout = 1)
            counter += 1
            if counter > 10:
                self.running.Write("echo %s\n" % (endPrompt))
        self.running.CbDelOnFdRead(self.logOutputPkgCatUpdate)
        return self.PkgCatInstalled
    def installPackage(self,package):  
        
        
        self.running.CbAddOnFdRead(self.logOutputPkg)
        passenv_ignored = set(["PATH","SHLVL","OLDPWD","PS1"])
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptPkgInstallStart = re.compile(startPrompt)
        self.promptPkgInstallEnd = re.compile(endPrompt)
        self.log.info("promptPkgInstallStart %s" %(startPrompt))
        self.log.info("promptPkgInstallEnd %s" %(endPrompt))
        
        self.waitingOnPromptPkgInstallStart = True
        self.waitingOnPromptPkgInstallEnd = False
        self.running.Write("echo %s\n" % (startPrompt))
        counter = 0
        


        cmd = 'apt-get install -y %s\n' % (package)
        self.log.info("PkgInstall %s" %(cmd.strip()))
        self.running.Write(cmd)
        self.log.info("PkgInstall %s" %(cmd.strip()))
        self.running.Comunicate(timeout = 1)
        self.running.Write("echo %s\n" % (endPrompt))
        
        while self.waitingOnPromptPkgInstallEnd == True:
            self.running.Comunicate(timeout = 1)
        self.running.CbDelOnFdRead(self.logOutputPkg)
        
        return True
    
    
    
    def installPackages(self,packages):
        notinstalled = set([])
        insalledPkg = self.updatePackages()
        for pack in packages:
            if pack in insalledPkg:
                print pack, pack in insalledPkg
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
        
        
    def finalise(self):
        if self.running.returncode == None:
            self.running.Write("exit 0\n")




class ChrootPackageInstallerRedhat(object):

    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        self.log = logging.getLogger("ChrootPackageInstallerDebian2")
        self.chrootCmd = kwargs.get('command', None)
        self.logOut = logging.getLogger("pkg.out")
        self.logErr = logging.getLogger("pkg.err")
        
    
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
            foundpackages.add(cleanline)
            #print fred
            #self.logOutput(fd,data,args,keys)
        
        return True
    def logOutputPkginstall(self,fd,data,args,keys):    
        pass
    def initialise(self):
        if self.chrootCmd == None:
            self.log.error("No chroot command set")
            return False
        self.running = watcher.LogRunShell(command=self.chrootCmd)
        self.running.Start()
        self.running.Write("set -x \n")
        self.running.Write("set -e \n")
        
    def updatePackages(self):
        self.waitingOnPromptPkgCatUpdateEnd = False
        
        self.waitingOnPromptPkgCatUpdateStart = True
        self.PkgCatInstalled = set([])
        #self.shell.Write("apt-get update -y\n")
        cmd = "rpm -qa --qf '%{NAME}\n'\n"
        self.running.CbAddOnFdRead(self.logOutputPkgCatUpdate)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        
        self.promptPkgCatUpdateStart = re.compile(startPrompt)
        self.promptPkgCatUpdateEnd = re.compile(endPrompt)
        
        self.running.Write("echo %s\n" % (startPrompt))
        while self.promptPkgCatUpdateStart == True:
            self.running.Comunicate(timeout = 1)
        self.running.Write("%s\n" % (cmd))
        self.running.Write("echo %s\n" % (endPrompt))
        self.waitingOnPromptPkgCatUpdateEnd = True
        while self.waitingOnPromptPkgCatUpdateEnd == True:
            self.running.Comunicate(timeout = 1)
        self.running.CbDelOnFdRead(self.logOutputPkgCatUpdate)
        return self.PkgCatInstalled
    def installPackage(self,package):  
        self.log.info("installPackage")
        
        self.running.CbAddOnFdRead(self.logOutputPkg)
        passenv_ignored = set(["PATH","SHLVL","OLDPWD","PS1"])
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptPkgInstallStart = re.compile(startPrompt)
        self.promptPkgInstallEnd = re.compile(endPrompt)
        self.log.info("promptPkgInstallStart %s" %(startPrompt))
        self.log.info("promptPkgInstallEnd %s" %(endPrompt))
        
        self.waitingOnPromptPkgInstallStart = True
        self.waitingOnPromptPkgInstallEnd = False
        self.running.Write("echo %s\n" % (startPrompt))
        counter = 0
        
        cmd = "yum install -y -q %s\n" % (package)
        self.log.info(cmd.strip())
        self.log.info("PkgInstall %s" %(cmd.strip()))
        self.running.Write(cmd)
        self.log.info("PkgInstall %s" %(cmd.strip()))
        self.running.Comunicate(timeout = 1)
        self.running.Write("echo %s\n" % (endPrompt))
        
        while self.waitingOnPromptPkgInstallEnd == True:
            self.running.Comunicate(timeout = 1)
        self.running.CbDelOnFdRead(self.logOutputPkg)
        
        return True
    
    
    
    def installPackages(self,packages):
        notinstalled = set([])
        insalledPkg = self.updatePackages()
        for pack in packages:
            if pack in insalledPkg:
                print pack, pack in insalledPkg
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
        
        
    def finalise(self):
        if self.running.returncode == None:
            self.running.Write("exit 0\n")


