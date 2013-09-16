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
        if self.running.returncode == None:
            self.running.Write("exit 0\n")

