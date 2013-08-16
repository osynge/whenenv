import logging
import uuid
import base64
import string
import watcher
import prompts
import re
import observable
import time
import datetime

transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )


syncDelay = datetime.timedelta(seconds=100)
timeoutDelay = datetime.timedelta(seconds=1500)




class runnershell2(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("runshell")
        self.chrootCmd = kwargs.get('command', None)
        #self.log.info("chrootCmd=%s" % (self.chrootCmd))
        self.env = kwargs.get('env', {})
        self.running = None
        self.logOut = logging.getLogger("sr2.out")
        self.logErr = logging.getLogger("sr2.err")
        self.state = observable.Observable(None)
    
    
    def bunpSyncTime(self,Now):
        self.SyncTime = Now + syncDelay
    
    
    def logOutput(self,fd,data,args,keys):
        log = self.log
        if fd == 1:
            log = self.logOut
        if fd == 2:
            log = self.logErr
        for line in data.split('\n'):
            if len(line) > 0:
                log.info(line)
        
    def ScriptOnExit(self,pid,rc,args,keys):
        self.log.info("Script %s exited early with %s" %(pid,rc))
        self.waitingOnPromptRunScriptEnd = False
        
        self.waitingOnPromptGetEnvEnd = False
        
        
    def logOutputSetEnv(self,fd,data,args,keys):
        #self.logOutput(fd,data,args,keys
        Now = datetime.datetime.now()
        self.bunpSyncTime(Now)
        lines = data.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            if self.waitingOnPromptSetEnvEnd == True:
                matches = self.promptSetEnvEnd.match(line)
                if matches != None:
                    self.waitingOnPromptSetEnvEnd = False
                    continue
            if self.waitingOnPromptSetEnvStart == True:
                matches = self.promptSetEnvStart.match(line)
                if matches != None:
                    self.waitingOnPromptSetEnvStart = False
                    self.waitingOnPromptSetEnvEnd = True
                    continue
                
            else:
                if not self.waitingOnPromptSetEnvEnd == True:
                    # We only want lines after the start
                    continue
                # Any line that gets here is a suprise
                
            
        
        
    def logOutputRunScript(self,fd,data,args,keys):
        #self.logOutput(fd,data,args,keys)
        Now = datetime.datetime.now()
        self.bunpSyncTime(Now)
        lines = data.split('\n')
        for line in lines:
            cleanline = line.strip()
            if len(cleanline) == 0:
                continue
            if self.waitingOnPromptRunScriptEnd == True:
                matches = self.promptRunScriptEnd.match(line)
                if matches != None:
                    self.waitingOnPromptRunScriptEnd = False
                    continue
            if self.waitingOnPromptRunScriptStart == True:
                matches = self.promptRunScriptStart.match(line)
                if matches != None:
                    self.waitingOnPromptRunScriptStart = False
                    self.waitingOnPromptRunScriptEnd = True
                    continue
                
            self.logOutput(fd,cleanline,args,keys)
            
         
        
        
    def logOutputGetEnv(self,fd,data,args,keys):
        lines = data.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            if self.waitingOnPromptGetEnvEnd == True:
                matches = self.promptGetEnvEnd.match(line)
                if matches != None:
                    self.waitingOnPromptGetEnvEnd = False
                    continue
            if self.waitingOnPromptGetEnvStart == True:
                matches = self.promptGetEnvStart.match(line)
                if matches != None:
                    self.waitingOnPromptGetEnvStart = False
                    self.waitingOnPromptGetEnvEnd = True
                    continue
            else:
                if not self.waitingOnPromptGetEnvEnd == True:
                    # We only want lines after the start
                    continue
                if fd != 1:
                    continue
                cleanline = line.strip()
                splitline = cleanline.split('=')
                if len(splitline) < 2:
                    continue
                tail = splitline[1:]
                #self.logOutput(fd,line,args,keys)
                self.FoundEnv[splitline[0]] = splitline[1]
            
    
    def initialise(self):
        if self.chrootCmd == None:
            self.log.error("No chroot command set")
            return False
        self.running = watcher.LogRunShell(command=self.chrootCmd)
        self.running.Start()
        self.running.Write("set -x \n")
        self.running.Write("set -e \n")
        return True
    def runscript(self,script):
        if None != self.running.returncode():
            return None
        self.running.CbAddOnExit(self.ScriptOnExit)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptRunScriptStart = re.compile(startPrompt)
        self.promptRunScriptEnd = re.compile(endPrompt)
        self.waitingOnPromptRunScriptStart = True
        self.waitingOnPromptRunScriptEnd = False
        Now = datetime.datetime.now()
        self.bunpSyncTime(Now)
        TimeOutTime = timeoutDelay + Now
        self.running.CbAddOnFdRead(self.logOutputRunScript)
        self.running.Write("echo %s\n" % (startPrompt))
        while self.waitingOnPromptRunScriptStart == True:
            self.running.Comunicate(timeout = 1)
            Now = datetime.datetime.now()
            if Now > self.SyncTime:
                self.log.error("echo sync")
                self.running.Write("echo %s\n" % (startPrompt))
                self.bunpSyncTime(Now)
            if Now > TimeOutTime:
                self.log.error("runscript time out 1")
                break
        fp = open(script)
        for line in fp:
            cleanline = line.strip()
            self.log.debug("run+%s" %(cleanline))
            self.running.Write(line)
        self.running.Write("echo %s\n" % (endPrompt))
        counter = 0
        while self.waitingOnPromptRunScriptEnd == True:
            self.running.Comunicate(timeout=1)
            Now = datetime.datetime.now()
            if Now > self.SyncTime:
                self.bunpSyncTime(Now)
                self.running.Write("echo %s\n" % (endPrompt))
            if Now > TimeOutTime:
                self.log.error("runscript time out 2")
                break
        self.running.CbDelOnFdRead(self.logOutputRunScript)
        self.running.CbDelOnExit(self.ScriptOnExit)
        rc = 0
        
        if not self.running.returncode() == None:
             rc = self.running.returncode()
        return rc
        
        
        
    def setEnv(self,env):
        self.running.CbAddOnFdRead(self.logOutputSetEnv)
        passenv_ignored = set(["PATH","SHLVL","OLDPWD","PS1"])
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptSetEnvStart = re.compile(startPrompt)
        self.promptSetEnvEnd = re.compile(endPrompt)
        self.waitingOnPromptSetEnvStart = True
        self.waitingOnPromptSetEnvEnd = False
        self.running.Write("echo %s\n" % (startPrompt))
        counter = 0
        while self.waitingOnPromptSetEnvStart == True:
            self.running.Comunicate(timeout = 1)
            counter += 1
            if counter > 100:
                counter = 0
                self.running.Write("echo %s\n" % (startPrompt))
        for enviroment in env.keys():
            if enviroment in passenv_ignored:
                continue
            cmd = '%s="%s"\n' % (enviroment,env[enviroment])
            #self.log.info("setEnv %s" %(cmd))
            self.running.Write(cmd)
        self.running.Write("echo %s\n" % (endPrompt))
        while self.waitingOnPromptSetEnvEnd == True:
            self.running.Comunicate(timeout = 1)
        self.running.CbDelOnFdRead(self.logOutputSetEnv)
        return True
        
    def getEnv(self):
        if None != self.running.returncode():
            self.log.info("returning none %s" %("ddd"))
            return None
        self.FoundEnv = {}
        output = {}
        self.running.CbAddOnExit(self.ScriptOnExit)
        self.running.CbAddOnFdRead(self.logOutputGetEnv)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptGetEnvStart = re.compile(startPrompt)
        self.promptGetEnvEnd = re.compile(endPrompt)
        self.running.Comunicate(timeout=1)
        self.waitingOnPromptGetEnvStart = True
        self.waitingOnPromptGetEnvEnd = False
        cmd = "echo %s\n" % (startPrompt)
        self.running.Write(cmd)
        while self.waitingOnPromptGetEnvStart == True:
            self.running.Comunicate()
        self.FoundEnv = {}
        self.running.Write("env\n")
        self.running.Write("echo %s\n" % (endPrompt))
        counter = 0 
        while self.waitingOnPromptGetEnvEnd == True:
            counter += 1
            if counter > 100:
                counter = 0
                self.running.Write("echo %s\n" % (endPrompt))
            self.running.Comunicate()
        self.running.CbDelOnFdRead(self.logOutputGetEnv)
        self.running.CbDelOnExit(self.ScriptOnExit)
        self.log.debug("getEnv end")
        return self.FoundEnv
    def finalise(self):
        if self.running.returncode == None:
            self.running.Write("exit 0\n")
        self.running.Comunicate(timeout=1)
        if self.running.returncode == None:
            self.running.Write("exit 0\n")
        self.running.Comunicate(timeout=1)
        if self.running.returncode == None:
            self.running.Write("exit 0\n")
        self.running.Comunicate(timeout=1)
        if self.running.returncode == None:
            self.running.Write("exit 0\n")
        self.running.Comunicate(timeout=1)
        
