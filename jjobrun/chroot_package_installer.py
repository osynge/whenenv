
class ChrootPackageInstaller:
    def __init__(self, chrootCmd, env):
        self.log = logging.getLogger("ChrootPackageInstaller")
        self.chrootCmd = chrootCmd
        match_prompt = uuid.uuid1()
        self.prompt = base64.b32encode(str(match_prompt).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        self.env = env
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
        
