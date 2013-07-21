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


class ChrootPackageInstaller:
    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        
        self.cartridge_state =  "non-empty"
        self.log = logging.getLogger("ChrootPackageInstaller")
        self.chrootCmd = kwargs.get('command', None)
        match_prompt = uuid.uuid1()
        self.prompt = base64.b32encode(str(match_prompt).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        self.env = kwargs.get('enviroment', None)
        self.log.info("self.env=%s" % (self.env))
        self.p = None
    def initialise(self):
        self.log.info("Initialising:%s" % (self.chrootCmd))
        if self.chrootCmd == None:
            self.log.error("chrootCmd=None")
            return False
        self.p = pexpect.spawn(self.chrootCmd)
        self.p.send("\nstty -echo\n")
        self.p.flush()
        
        self.p.send("PS1=%s\n" % (self.prompt))
        done = False
        while done == False:
            index = self.p.expect ([self.prompt, 
                    pexpect.EOF, 
                    pexpect.TIMEOUT],timeout=500)
            if index == 0:
                done = True
            else:
                self.log.error("Somethign went wrong entering chroot %s=%s" % (index,self.chrootCmd))
                self.p = None
                return False
        self.p.flush()
        self.log.info("Initialising succeded")
        return True
    
        
    def updatePackages(self):
        if self.p == None:
            self.log.error("programming error no p")
            return False
        self.p.flush()
        self.p.send("rpm -qa --qf '%{NAME}\n'\n")
        done = False
        packagelist = []
        while done == False:
            index = self.p.expect ([self.prompt,
                    '\r\n', 
                    pexpect.EOF, 
                    pexpect.TIMEOUT],timeout=500)
            if index == 0:
                done = True
            elif index == 1:
                packagelist.append(self.p.before)
                self.log.debug("before=%s" % (self.p.before))
                self.log.debug("after=%s" % (self.p.after))
            else:
                self.log.error("Somethign went wrong entering chroot")
                self.p = None
                return False
        self.packagelist = packagelist
        return self.packagelist
    def installPackages(self,packagelist):
        packagesFound = self.updatePackages()
        needtoInstall = []
        for package in packagelist:
            if package in packagesFound:
                self.log.info("already installed:%s" % (package))
            else:
                self.log.info("not installed:%s" % (package))
                needtoInstall.append(package)
        for package in needtoInstall:
            self.p.flush()
            cmd = "yum install -y -q %s" % (package)
            self.log.info("running :%s" % (cmd))
            self.p.send(cmd + '\n')
            done = False
            while done == False:
                index = self.p.expect ([self.prompt,
                        '\r\n', 
                        pexpect.EOF, 
                        pexpect.TIMEOUT],timeout=500)
                if index == 0:
                    done = True
                elif index == 1:
                    self.log.info(self.p.before)
                else:
                    self.log.error("Somethign went wrong entering chroot")
                    self.p = None
                    return False
            # so now the command has executed
            self.p.flush()
            # We now need to see teh RC
            self.log.info("checking execution status")
            self.p.send("echo $?\n")
            rc = ""
            done = False
            while done == False:
                index = self.p.expect ([self.prompt,
                        '\r\n', 
                        pexpect.EOF, 
                        pexpect.TIMEOUT],timeout=500)
                if index == 0:
                    done = True
                elif index == 1:
                    
                    rc += self.p.before
                else:
                    self.log.error("Somethign went wrong entering chroot")
                    self.p = None
                    return False
            if rc != '0':
                self.log.error("rc=%s" % (rc))
                return False
        # Now we check all packages are installed
        packagesFound = self.updatePackages()
        needtoInstall = []
        for package in packagelist:
            if package in packagesFound:
                self.log.info("already installed:%s" % (package))
            else:
                self.log.info("not installed:%s" % (package))
                needtoInstall.append(package)     
        if len(needtoInstall) > 0:
            self.log.error("The following packages did not install:%s" % (needtoInstall))
            return False
        return True
        
class ChrootPackageInstallerRedhatOld(ChrootPackageInstaller):

    def __init__(self,  *args, **kwargs):
        ChrootPackageInstaller.__init__(self,*args, **kwargs)
        self.log = logging.getLogger("ChrootPackageInstallerRedhat")
        
 
    def updatePackages(self):
        if self.p == None:
            self.log.error("programming error no p")
            return False
        self.p.flush()
        self.p.send("rpm -qa\n")
        done = False
        packagelist = []
        while done == False:
            index = self.p.expect ([self.prompt,
                    '\r\n', 
                    pexpect.EOF, 
                    pexpect.TIMEOUT],timeout=500)
            if index == 0:
                done = True
            elif index == 1:
                packagelist.append(self.p.before)
                self.log.debug("before=%s" % (self.p.before))
                self.log.debug("after=%s" % (self.p.after))
            else:
                self.log.error("Somethign went wrong entering chroot")
                self.p = None
                return False
        self.packagelist = packagelist
        self.log.info("Number of packages installed=%s" % (len(self.packagelist)))
        return self.packagelist
        
    def installPackages(self,packagelist):
        packagesFound = self.updatePackages()
        needtoInstall = []
        for package in packagelist:
            if package in packagesFound:
                self.log.info("already installed:%s" % (package))
            else:
                self.log.info("not installed:%s" % (package))
                needtoInstall.append(package)
        for package in needtoInstall:
            self.p.flush()
            cmd = "yum install -y -q %s" % (package)
            self.log.info("running :%s" % (cmd))
            self.p.send(cmd + '\n')
            done = False
            while done == False:
                index = self.p.expect ([self.prompt,
                        '\r\n', 
                        pexpect.EOF, 
                        pexpect.TIMEOUT],timeout=500)
                if index == 0:
                    done = True
                elif index == 1:
                    self.log.info(self.p.before)
                else:
                    self.log.error("Somethign went wrong entering chroot")
                    self.p = None
                    return False
            # so now the command has executed
            self.p.flush()
            # We now need to see teh RC
            self.log.info("checking execution status")
            self.p.send("echo $?\n")
            rc = ""
            done = False
            while done == False:
                index = self.p.expect ([self.prompt,
                        '\r\n', 
                        pexpect.EOF, 
                        pexpect.TIMEOUT],timeout=500)
                if index == 0:
                    done = True
                elif index == 1:
                    
                    rc += self.p.before
                else:
                    self.log.error("Somethign went wrong entering chroot")
                    self.p = None
                    return False
            if rc != '0':
                self.log.error("rc=%s" % (rc))
                return False
        # Now we check all packages are installed
        packagesFound = self.updatePackages()
        needtoInstall = []
        for package in packagelist:
            if package in packagesFound:
                self.log.info("already installed:%s" % (package))
            else:
                self.log.info("not installed:%s" % (package))
                needtoInstall.append(package)     
        if len(needtoInstall) > 0:
            self.log.error("The following packages did not install:%s" % (needtoInstall))
            return False
        return True
        
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
            #self.logOutput(fd,data,args,keys)
        
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
        self.running.Write("echo %s\n" % (endPrompt))
        self.waitingOnPromptPkgCatUpdateEnd = True
        while self.waitingOnPromptPkgCatUpdateEnd == True:
            self.running.Comunicate(timeout = 1)
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


class ChrootPackageInstallerRedhat(ChrootPackageInstaller):
    def __init__(self, *args, **kwargs):
        # we still need these things chrootCmd, env):
        self.log = logging.getLogger("ChrootPackageInstallerDebian2")
        self.chrootCmd = kwargs.get('command', None)
        self.logOut = logging.getLogger("pkg.out")
        self.logErr = logging.getLogger("pkg.err")
    def installPackages(self,packages):
        self.running.CbAddOnFdRead(self.logOutput)
        passenv_ignored = set(["PATH","SHLVL","OLDPWD","PS1"])
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptPkgInstallStart = re.compile(startPrompt)
        self.promptPkgInstallEnd = re.compile(endPrompt)
        self.log.info("promptPkgInstallStart %s" %(self.promptPkgInstallStart))
        self.log.info("promptPkgInstallEnd %s" %(self.promptPkgInstallEnd))
        
        self.waitingOnPromptPkgInstallStart = True
        self.waitingOnPromptPkgInstallEnd = False
        self.running.Write("echo %s\n" % (startPrompt))
        counter = 0
        
        for enviroment in packages:
            
            cmd = 'yum install -y %s\n\n' % (enviroment)
            self.running.Comunicate(timeout = 1)
            self.log.info("PkgInstall %s" %(cmd))
            self.running.Write(cmd)
        self.running.Write("echo %s\n" % (endPrompt))
        while self.waitingOnPromptPkgInstallEnd == True:
            self.running.Comunicate(timeout = 1)
        self.running.CbDelOnFdRead(self.logOutput)
        return True
