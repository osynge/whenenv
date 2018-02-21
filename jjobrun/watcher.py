import logging
import uuid
import base64
import subprocess
import fcntl
import os
import time
import select
from . import observable
from . import prompts

def subphandling(cmd,timeout = 10):   
    log = logging.getLogger("sub")
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processRc = None
    handleprocess = True
    counter = 0
    stdout = ''
    stderr = ''
    while handleprocess:
        counter += 1
        time.sleep(1)
        cout,cerr = process.communicate()
        stdout += cout
        stderr += stderr
        log.info(cout)
        log.warning(cerr)
        process.poll()
        processRc = process.returncode
        if processRc != None:
            break
        if counter == timeout:
            os.kill(process.pid, signal.SIGQUIT)
        if counter > timeout:
            os.kill(process.pid, signal.SIGKILL)
            processRc = -9
            break
    return (processRc,stdout,stderr)
    
    
    
    
    
class runshell(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("runshell")
        
        # we still need these things chrootCmd, env):
        
        self.cartridge_state =  "non-empty"
        self.log = logging.getLogger("ChrootPackageInstaller")
        self.chrootCmd = kwargs.get('command', None)
        self.prompt = prompts.GeneratePrompt()
        
        
        self.env = kwargs.get('enviroment', None)
        self.p = None
        self.OnFd = {}
        self.OnExitCb = {}
        
        
        command = None
        if "command" in kwargs.keys():
            command = kwargs["command"]
        
        
        self.cmd = observable.Observable(command)
    
    def CbAddOnExit(self,functionPtr,*args, **kwargs):
        self.OnExitCb[functionPtr] =  (args, kwargs)
    def CbDelOnExit(self,functionPtr):
        del self.OnExitCb[functionPtr]  
    def CbAddOnFdRead(self,functionPtr,*args, **kwargs):
        self.OnFd[functionPtr] =  (args, kwargs)
    def CbDelOnFdRead(self,functionPtr):
        del self.OnFd[functionPtr]
    
    def doCallBackFileDescriptor(self,Fd,Data):
        #self.log.info("out=%s,%s" % (Fd,Data))
        if len(Data) == 0:
            return
        for func in self.OnFd:
            func(Fd,Data,self.OnFd[func][0],self.OnFd[func][1])
    def doCallBackExit(self,pid,exitcode):
        #self.log.info("out=%s,%s" % (Fd,Data))
        for func in self.OnExitCb:
            func(pid,exitcode,self.OnExitCb[func][0],self.OnExitCb[func][1])
    
    
    
    
    
    def Start(self):
        log = logging.getLogger("sub")
    
        tsring = str(self.cmd.get())
        self.log.debug("cmdin=%s" % (tsring))
        self.fdMapping = {}
        self.process = subprocess.Popen([tsring], shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOutfd = self.process.stdout.fileno()
        self.fdMapping[stdOutfd] = 1
        stdErrfd = self.process.stderr.fileno()
        self.fdMapping[stdErrfd] = 2
        
        fl = fcntl.fcntl(stdOutfd, fcntl.F_GETFL)
        fcntl.fcntl(stdOutfd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        
        stdErrfd = self.process.stderr.fileno()
        fl = fcntl.fcntl(stdErrfd, fcntl.F_GETFL)
        fcntl.fcntl(stdErrfd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        #self.process.stdin.write("echo jam\n")
        #self.process.stdin.write("exit 0\n")
        
    def Comunicate(self,**kwargs):
        #cout,cerr = self.process.communicate()
        #self.doCallBackFileDescriptor(0,cout)
        #self.doCallBackFileDescriptor(1,cerr)
        timeout = kwargs.get('timeout', None)
        self.log.debug("her%s" % (self.process))
        self.log.debug("cmd='%s'" % (self.cmd.get()))
        self.log.debug("returncode='%s'" % (self.returncode()))
        self.log.debug("poll='%s'" % ( self.process.poll()))
        self.log.debug("timeout='%s'" % (type(timeout)))
        
        readFds,writeWds,exFds = select.select([ self.process.stderr,self.process.stdout],[],[],timeout)
        
        #self.log.debug("selected_read='%s'" % (readFds))
        #self.log.debug("selected_write='%s'" % (writeWds))
        #self.log.debug("selected_ex='%s'" % (exFds))
        for item in readFds:
            recivedFd = self.fdMapping[item.fileno()]
            newdata = item.read()
            self.doCallBackFileDescriptor(recivedFd,newdata)
        rc = self.returncode()
        if None != rc:
            self.doCallBackExit(self.process.pid,rc)
        self.log.debug("returncode='%s'" % (self.returncode()))
        #stdOutfd = self.process.stdout.fileno()
        #self.log.info("stdOutfd='%s'" % (stdOutfd))
        #readtext = self.process.stdout.read()
        #self.log.info("readtext='%s'" % (readtext))
        #readtext = self.process.stderr.read()
        #self.log.info("readtext='%s'" % (readtext))
        #self.doCallBackFileDescriptor(0,readtext)
        
        
    def returncode(self):
        if self.process.returncode == None:
            return None
        return self.process.returncode
    
    def Write(self,text):
        if self.process.returncode == None:
            self.process.stdin.write(text)
            self.log.debug("writing to a closed process")
            return True
        return False
            
    def wait(self):
        self.process.wait()

class LogRunShell(runshell):
    def __init__(self, *args, **kwargs):
        super(LogRunShell, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("LogRunShell")
    
    
    
    def logByFileDescriptor(self):
        self.log.error("failed to init CHROOT")
