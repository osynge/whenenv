
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
    log = logging.getLogger("callback")
    log.info("inpute=%s" % (inpute))

    log.info("data=%s" % (data.strip()))
    log.info("values=%s" % (len(args)))
    log.info("keys=%s" % (keys))
    
    




def t3():
    command="set -e\n"
    command="ls\n"
    command="echo tessssssssst && sleep 1 && exit 1\n"
    shell = jjobrun.watcher.LogRunShell(command=command)
    shell.CbAddOnFdRead(callback,1,2,cmd="sdsdsd")
    shell.Start()
    shell.returncode()
    counter = 0
    while shell.returncode() == None:
        shell.Comunicate()
        time.sleep(0.1)
        counter += 1
        if counter > 400:
            exit (0)

t3()

