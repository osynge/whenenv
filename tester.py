
from jjobrun.chroot_package_installer import ChrootPackageInstallerRedhat ,ChrootPackageInstallerDebian
from jjobrun.chroot_script_runner import runnershell
import jjobrun.watcher
import logging
import time

logging.basicConfig(level=logging.INFO)
def t1():
    foo = ChrootPackageInstallerDebian(command="/bin/bash")
    foo.initialise()
    output = foo.updatePackages()
    print len(output)


def t2():
    foo = runnershell("/bin/bash",{})
    foo.initialise()
    script = "transfer/GenChroot.SL-6X.sh"
    print foo.getEnv()
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
    command="ls\n"
    #command="echo tessssssssst && sleep 1 && exit 1\n"
    command="bash\n"
    shell = jjobrun.watcher.LogRunShell(command=command)
    shell.CbAddOnFdRead(callback,1,2,cmd="sdsdsd")
    shell.CbAddOnExit(callbackExit)
    shell.Start()
    shell.Write("set -e\n")
    shell.Write("PS1=hello\n")
    
    shell.Write("apt-get update\n")
    shell.Write("echo dddddd=$?\n")
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
        shell.Comunicate()
        time.sleep(0.1)
        counter += 1
        if counter > 400:
            exit (0)
    print shell.returncode()
t3()

