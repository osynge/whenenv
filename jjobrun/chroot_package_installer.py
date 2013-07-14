import logging
import uuid
import base64
import string
import pexpect
import re
transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )
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
        
class ChrootPackageInstallerRedhat(ChrootPackageInstaller):

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
        
class ChrootPackageInstallerDebian(ChrootPackageInstaller):

    def __init__(self,  *args, **kwargs):
        #super(ChrootPackageInstallerDebian, self).__init__(*args, **kwargs)
        ChrootPackageInstaller.__init__(self,*args, **kwargs)
        self.log = logging.getLogger("ChrootPackageInstallerDebian")
        
        
    def updatePackages(self):
        if self.p == None:
            self.log.error("programming error no p")
            return False
        self.p.flush()
        self.p.send("/usr/bin/dpkg-query -W ${Package}\t${Status}\n")
        match1 = "\tinstall ok installed\r\n"
        match1 = "deinstall ok config-files\r\n"
        done = False
        packagelist = []
        while done == False:
            index = self.p.expect ([match1,self.prompt,
                    '\r\n', 
                    pexpect.EOF, 
                    pexpect.TIMEOUT],timeout=500)
            if index == 0:
                self.log.debug("xxbefore=%s" % (self.p.before))
                self.log.debug("xxafter=%s" % (self.p.after))
            if index == 1:
                done = True
            elif index == 2:
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
            match_one =  uuid.uuid1()
            bashvar_one = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
            match_two =  uuid.uuid1()
            bashvar_two = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
            self.p.send("echo %s\n" % bashvar_one)
            index = self.p.expect ([bashvar_one,pexpect.EOF, pexpect.TIMEOUT],timeout=10)
            cmd = "apt-get install -y --force-yes -q 3 %s\n" % (package)
            self.p.send(cmd + '\n')
            self.p.send("echo %s\n" % bashvar_two)
            self.log.info("running :%s" % (cmd))
            
            
            done = False
            while done == False:
                index = p.expect (["Do you want to continue",
                    bashvar_two,
                    "%s is already the newest version." % (package),
                    "additional disk space will be used", 
                    pexpect.EOF, 
                    pexpect.TIMEOUT,
                    'Reading package lists',
                    'The following NEW packages will be installed',
                    'Get:.*\r\n',
                    'Selecting previously unselected package',
                    'Fetched',
                    'Unpacking',
                    'Setting',
                    'Processing triggers for ', '\r\n'],
                    timeout=500)
                self.log.info("whatsDaProb=%s" % (index))
                if index == 0:
                    p.send("Y\n")
                    
                if index >= 6:
                    imput = p.before
                    striped = imput.strip()
                    if len(striped) > 0:
                        self.log.info(imput.strip())
                if index in [2,4]:
                    done = True
                if index == 3:
                    p.send("Y\n")
                if index == 1:
                    done = True
            

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
    
    def packagesDebain(self,jobpart,env):
        depnedacylist = []
        if "shell" in jobpart.keys():
            
            if "dependancies" in jobpart["shell"].keys():
                
                if "Debian" in jobpart["shell"]["dependancies"].keys():
                    self.log.info("foundthe answer")
                    depnedacylist = list(jobpart["shell"]["dependancies"]["Debian"])
        if len(depnedacylist) == 0:
            return True
        
        #script_filename = "foo"
        #if os.path.isfile(script_filename):
        #    fout = file (script_filename, "ab")
        #else:
        #    fout = file (script_filename, "wb")
        #self.p.logfile = fout
        match_prompt = uuid.uuid1()
        prompt = str(match_prompt)
        packagesmissing = []
        alreadyinstalled = []
        for package in depnedacylist:
            self.log.info("todo=%s" % (package))
            cmd = "/usr/sbin/chroot $CHROOT /usr/bin/dpkg-query -W --showformat='${Status}\n' %s\n" % (package)
            p = pexpect.spawn(cmd)
            p.send("PS1=%s\n" % (prompt)) 
            p.send(cmd)
            
            done = False
            while done == False:
                index = p.expect (["Do you want to continue",
                    prompt,
                    "%s is already the newest version." % (package),
                    "additional disk space will be used", 
                    pexpect.EOF, 
                    pexpect.TIMEOUT,
                    'Reading package lists',
                    'The following NEW packages will be installed',
                    'Get:.*\r\n',
                    'Selecting previously unselected package',
                    'Fetched',
                    'Unpacking',
                    'Setting',
                    'Processing triggers for ', '\r\n'],
                    timeout=500)
                self.log.info("whatsDaProb=%s" % (index))
                if index == 0:
                    p.send("Y\n")
                    
                if index >= 6:
                    imput = p.before
                    striped = imput.strip()
                    if len(striped) > 0:
                        self.log.info(imput.strip())
                if index in [2,4]:
                    done = True
                if index == 3:
                    p.send("Y\n")
                if index == 1:
                    p.send(cmd)
           
            exitstatus = p.exitstatus
            if p.isalive() == True:
                p.send("exit 0\n")
            if p.isalive() == True:
                p.wait()
                
        for package in depnedacylist:
            #self.log.info("ssssssssssssssssssssssssssssssssss")
            cmd = "/usr/sbin/chroot $CHROOT  /usr/bin/apt-get install -y --force-yes %s\n" % (package)
            self.log.info(cmd)
            p = pexpect.spawn(cmd)
            p.send("PS1=%s\n" % (self.prompt)) 
            p.send(cmd)
            done = False
            while done == False:
                index = p.expect (["Do you want to continue",
                    prompt,
                    "%s is already the newest version." % (package),
                    "additional disk space will be used", 
                    pexpect.EOF, 
                    pexpect.TIMEOUT,
                    'Reading package lists',
                    'The following NEW packages will be installed',
                    'Get:.*\r\n',
                    'Selecting previously unselected package',
                    'Fetched',
                    'Unpacking',
                    'Setting',
                    'Processing triggers for ', '\r\n'],
                    timeout=500)
                self.log.info("whatsDaProb=%s" % (index))
                if index == 0:
                    p.send("Y\n")
                    
                if index >= 6:
                    imput = p.before
                    striped = imput.strip()
                    if len(striped) > 0:
                        self.log.info(imput.strip())
                if index in [2,4]:
                    done = True
                if index == 3:
                    p.send("Y\n")
                if index == 1:
                    p.send(cmd)
            if p.isalive() == True:
                p.send("exit 0\n")
            if p.isalive() == True:
                p.wait()
            exitstatus = p.exitstatus
            self.log.error("exit status=%s, cmd=%s" % (exitstatus,cmd))
