from jjobrun.chroot_package_installer_rpm import ChrootPackageInstallerRedhat
from jjobrun.chroot_package_installer_deb import ChrootPackageInstallerDebian2
from jjobrun.chroot_script_runner import runnershell2
import jjobrun.watcher
import logging
import time

import unittest
logging.basicConfig(level=logging.INFO)
def t1():
    foo = ChrootPackageInstallerDebian(command="/bin/bash")
    foo.initialise()
    output = foo.updatePackages()
    print (len(output))


def t2():
    foo = runnershell("/bin/bash",{})
    foo.initialise()
    script = "transfer/GenChroot.SL-6X.sh"
    print (foo.getEnv())
    foo.p.send("echo PS1\n")
    foo.runscript("test.sh")


def callback(inpute,data,args,keys):
    log = logging.getLogger("callbackFd")
    #log.info("inpute=%s" % (inpute))

    log.info("%s:%s" % (inpute,data.strip()))
    #log.info("values=len(%s)" % (len(args)))
    #log.info("keys=%s" % (keys))
    
    
def callbackExit(rc,args,keys):
    log = logging.getLogger("callbackExit")
    if rc != 0:
        log.error("rc=%s" % (rc))
    log.info("values=len(%s)" % (len(args)))
    log.info("keys=%s" % (keys))
    
 



def t3():
    command="set -e\n"
    command="set -x\n"
    
    command="ls\n"
    #command="echo tessssssssst && sleep 1 && exit 1\n"
    command="bash\n"
    shell = jjobrun.watcher.LogRunShell(command=command)
    shell.CbAddOnFdRead(callback,1,2,cmd="sdsdsd")
    shell.CbAddOnExit(callbackExit)
    shell.Start()
    shell.Write("set -e\n")
    shell.Write("set -x\n")
    
    shell.Write("PS1=hello\n")
    
    shell.Write("apt-get update\n")
    shell.Write("export dddddd=$?\n")
    
    shell.Write("export\n")
    shell.Write("exit 0\n")
    #shell.Write("apt-get upgrade -y\n")
    #shell.Write("apt-get remove -y expat\n")
    #shell.Write("apt-get clean\n")
    #shell.Write("apt-get install -y expat\n")
    #script = "transfer/GenChroot.SL-6X.sh"
    #script = "transfer/GenChroot.debian-wheezy-part-03.sh"
    
    #for line in open(script):
    #    shell.Write(line)
    
    shell.Write("exit 0\n")
    
    #shell.process.stdin.write("echo jam\n")
    #shell.process.stdin.write("exit 2\n")
    
    counter = 0
    while shell.returncode() == None:
        shell.Comunicate(timeout=1)
        time.sleep(0.1)
        counter += 1
        if counter > 400:
            exit (0)
    print (shell.returncode())


def t4():
    foo = runnershell2(command = "/bin/bash")
    foo.initialise()
    foo.setEnv({ 'tang' : 'ssss'})
    script = "transfer/GenChroot.SL-6X.sh"
    print (foo.getEnv())
    foo.runscript(script)
    
def t5():
    chroot = "/workspace/chroot/executor_"
    foo = ChrootPackageInstallerDebian2(command = "chroot %s /bin/sh" % (chroot))
    foo.initialise()
    #foo.updatePackages()
    foo.installPackages(["git","make","rpm"])
    #foo.finalise()

#t4()
#t5()
import nose


class TestModule_runnershell2(unittest.TestCase):
    def test_initialise(self):    
        foo = runnershell2("/bin/bash",{})
        rc = foo.initialise()
        nose.tools.assert_equal(rc ,False)
