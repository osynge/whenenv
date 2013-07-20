import logging
import uuid
import base64
import pexpect
import string
import watcher
import prompts
import re
import observable

transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )

class runnershellOld:
    def __init__(self, chrootCmd, env):
        self.log = logging.getLogger("runnershell")
        self.chrootCmd = chrootCmd
        match_prompt = uuid.uuid1()
        self.prompt = base64.b32encode(str(match_prompt).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        self.env = env
        self.p = None
        self.watch = True
        self.cbBefore = None
        self.cbTimeOut = None
        self.watchTimer = 0
        self.watchTimerMax = 500
        
        
        
    
    def watcherTimedOut(self):
        if self.watchTimer > self.watchTimerMax:
            return True
        return False
    def watcherTimedIncrement(self):
        self.watchTimer += 2
    def watcherTimedDecrement(self):
        self.watchTimer -= 1
        #self.AliveChecks = {}

    def genWatcher(self):
        self.watch = True
        while self.watch == True:
            index = self.p.expect ([pexpect.EOF, pexpect.TIMEOUT],timeout=1)
            if index == 0:
                self.watch = False
            elif index == 1:
                before = self.p.before
                if self.cbBefore != None:
                    self.cbBefore(before,None)
                if self.cbTimeOut != None:
                    self.cbTimeOut(None)
    def delWatcher(self):
        self.watch = False
    
    def setPrompt(self):
        self.p.flush()
        match_one =  uuid.uuid1()
        bashvar_one = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        match_two =  uuid.uuid1()
        bashvar_two = base64.b32encode(str(match_two).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        
        sent = 'echo %s\n' % (bashvar_one)
        self.p.send(sent)
        index = self.p.expect ([bashvar_one,pexpect.EOF, pexpect.TIMEOUT],timeout=10)
        self.p.send("PS1=%s\\n\n" % (self.prompt))
        self.p.send("export PS1\n")
        self.p.flush()
        self.p.send("TERM=vt100\n")
        self.p.send("export TERM\n")
        
        sent = 'echo %s\n' % (bashvar_two)
        
        self.p.send(sent)
        done = False
        while done == False:
            index = self.p.expect ([bashvar_two, 
                    pexpect.EOF, 
                    pexpect.TIMEOUT],timeout=5)
            if index == 0:
                done = True
            elif index == 1:
                self.p.send(sent)
                self.log.info("prompt timeout=%s" % (index))
            else:
                self.log.info("prompt bad=%s" % (index))
                done = True       
        
        if index == 0:
            self.log.info("prompt Ok")
    
    def initialise(self):
        if None != self.p:
            self.finalise()
        self.log.info("Initialising:%s" % (self.chrootCmd))
        self.p = pexpect.spawn(self.chrootCmd)
        self.p.send("stty -echo\n")
        self.p.flush()
        self.setPrompt()
        return True
    def finalise(self):
        self.log.info("finalising")
        if self.p.isalive() == True:
            self.p.send("\nexit 0\n")
            self.p.flush()
        if self.p.isalive() == True:
            self.p.send("\nexit 0\n")
            self.p.flush()
        
        if self.p.isalive() == True:
            self.log.info("waiting")
            try:
                self.p.wait()
            except pexpect.ExceptionPexpect,E:
                self.log.error("pexpect.ExceptionPexpect:%s" % (E))
            
        exitstatus = self.p.exitstatus
        self.p = None
        self.log.info("finalising done")
        return exitstatus

    def setEnv(self,env):
        env_ignored = set(["PATH","SHLVL","OLDPWD","PS1"])
        for enviroment in env.keys():
            if enviroment in env_ignored:
                continue
            cmd = '%s="%s"\n' % (enviroment,env[enviroment])
            self.log.info("setEnv %s" %(cmd))
            self.p.send(cmd)
            self.p.flush()
        return True

    def getEnv(self):
        self.log.info("getEnv")
        env_ignored = set(["PATH","SHLVL","OLDPWD",])
        match_one =  uuid.uuid1()
        bashvar_one = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        match_two =  uuid.uuid1()
        bashvar_two = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        
        reuslts = {}
        self.p.send("\n")
        self.p.send("set +e\n")
        self.p.send("set +x\n")
        self.p.flush()
        self.p.send("echo %s\n" % bashvar_one)
        self.p.send("export\n")
        self.p.send("echo %s\n" % bashvar_two)
        self.p.flush()
        index = self.p.expect ([bashvar_one,pexpect.EOF, pexpect.TIMEOUT],timeout=100)
        match = 'declare -x '
        #ouput = self.p.read_nonblocking(timeout=100)
        #self.log.critical("ouput=%s" %(ouput))
        souldloop = True
        foundEnv = {}
        while souldloop == True:
            exitstatus = self.p.exitstatus
            if exitstatus != None:
                self.log.info("exitstatus=%s" % (exitstatus))
                self.log.info("self.p.env=%s" % self.p.env)
                break
            index = self.p.expect ([match,pexpect.EOF, pexpect.TIMEOUT,bashvar_two],timeout=20)
            self.log.debug("index=%s" %(index))
            if index == 0:
                imput = self.p.before
                if len(imput) == 0:
                    continue
                self.log.debug("dinggga=%s" % (imput))
                secondlevel = self.p.expect (['"\r\n',pexpect.EOF, pexpect.TIMEOUT],timeout=20)
                imput = self.p.before
                self.log.debug("secondlevel=%s=%s" % (secondlevel,imput))
                if secondlevel == 0:
                    imput = self.p.before
                    striped = imput.strip()
                    if len (striped) == 0:
                        continue
                    #self.log.info("secondlevel=%s" % (striped))
                    splitline = striped.split('="')
                    self.log.debug("splitline=%s" % (splitline))
                    if len(splitline) < 2:
                        
                        continue
                    key = splitline[0]
                    value = splitline[1]
                    if key in env_ignored:
                        continue
                    foundEnv[key] = value
            elif index == 1:
                break
            elif index == 2:
                break
            elif index == 3:
                self.log.info("ended")
                break
            else:
                self.log.info("error=%s" % (index))
        self.log.debug("getEnv returns=%s" % (foundEnv))
        return foundEnv
    
    def runscript(self,script):
        return self.runscript3(script)
    
    def displayMessage(self,message):
        lastlinelen = len(self.lastDispalyedLine)
        lines = message.split('\n')
        for line in lines:
            clenaline = line.strip()
            print 'diff="%s"' % (clenaline)
            if lastlinelen == len(clenaline):
                print "match"
            self.lastDispalyedLine = clenaline
        
    def runscript_beve_callback(self,before,userdata):
        self.watcherTimedDecrement()
    
        messageDiff = before[self.lastMessageLen:].strip()
        self.lastMessageLen = len(before)
        if len(messageDiff) > 0:
            self.displayMessage(messageDiff)
        slive = False
        for Line in messageDiff.split('\n'):
            firstLine = Line.strip()
            #print 'firstLine="%s"' % (firstLine)
            #print self.AliveChecks
            if firstLine in self.AliveChecks:
                slive = True
                break
        if slive:
            # We know the terminal is back
            self.scriptReturned = True
            self.AliveChecks = []
        
        
    
        
    
    
    def scriptReturnedCheck(self):
        match_one =  uuid.uuid1()
        bashvar_one = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        line2send = "echo %s\n" % (bashvar_one)
        self.p.send(line2send)
        self.AliveChecks.append(bashvar_one)
        if len (self.AliveChecks) > 10:
            self.AliveChecks.pop(0)
        
        
    def runscript_timeout_callback(self,userdata):
        self.watcherTimedIncrement()
        #print 'here=%s' % (self.readingline)
        if len(self.lines) > self.readingline:
            line2send = self.lines[self.readingline]
            self.log.info("sent=%s" % (line2send.strip()))
            self.p.send(line2send)
            self.readingline += 1
        else:
            if self.scriptReturned:
                self.delWatcher()
            else:
                self.reminderCounter += 1
                if self.reminderCounter > self.reminderCounterMax:
                    self.reminderCounter = 0
                    self.reminderCounterMax += 10
                    if self.scriptReturnedCheck():
                        self.log.info("sent scriptreturnCheck")
        #self.p.send("echo ls\n")
        
        
    def runscript3(self,script):
        self.log.info("runscript3(%s)" % (script))
        self.cbBefore = self.runscript_beve_callback
        self.cbTimeOut = self.runscript_timeout_callback
        self.lines = []
        self.readingline = 0
        self.scriptReturned = False
        self.lastMessageLen = 0
        self.AliveChecks = []
        self.reminderCounter = 0
        self.reminderCounterMax = 10
        self.lastDispalyedLine = ""
        fp = open(script)
        for line in fp:
            self.lines.append(line)
        
        self.genWatcher()
        exitstatus = self.p.exitstatus
        output = 0
        if exitstatus != None:
            self.log.info("runscript returns(%s)" % (exitstatus))
            output = exitstatus
        return output
    def runscript2(self,script):
        self.log.info("runscript(%s)" % (script))
        # Now load script
        fp = open(script)
        self.setPrompt()
        match_one =  uuid.uuid1()
        bashvar_one = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        self.p.flush()
        self.p.send("\nset -e\n")
        self.p.send("\nset -x\n")
        self.p.flush()
        self.setPrompt()
        for line in fp:
            self.p.send(line)
        sent = 'echo "%s$?%s"\n' % (bashvar_one,bashvar_one)
        self.log.info("sent='%s'" % (sent))
        self.p.send(sent)
        
        souldloop = True
        output = 0
        ready = False
        state = 0
        returnCode = None
        
        nextlinecount = 3
        timeouts = 0
        while souldloop == True:
            index = self.p.expect ([bashvar_one,self.prompt,pexpect.EOF, pexpect.TIMEOUT,""],timeout=5)
            self.log.debug("indexxx=%s" % (index))
            
            if index == 0:
                secondIndex = self.p.expect ([bashvar_one,self.prompt,pexpect.EOF, pexpect.TIMEOUT],timeout=5)
                
                if secondIndex == 0:
                    cleaned = self.p.before.strip()
                    
                    self.log.info("Got script RC value=%s" % (cleaned))
                    #output = int(cleaned)
                    break 
                else:
                    self.log.error("Failed retriving RC")
            if index == 1:
                imput = self.p.before
                striped = imput.strip()
                if len(striped) > 0:
                    self.log.info(imput.strip())
                timeouts = 0
                #self.p.send('echo %s="${?}"\n' % (bashvar_one))
            if index == 2:
                imput = self.p.before
                striped = imput.strip()
                if len(striped) > 0:
                    self.log.info(imput.strip())
                self.log.error("Unexpected EOF")
                exitstatus = self.p.exitstatus
                if exitstatus != None:
                    output = exitstatus
                else:
                    output = 255
                self.log.error("Quit")
                return output
                    
                
            if index == 3:
                self.log.debug("TimeOut")
                
                timeouts = timeouts +1
                if timeouts > 100:
                    self.log.error("timedout")
                    return output
            if index == 4:
                timeouts = 0
                imput = self.p.before
                striped = imput.strip()
                if len(striped) > 0:
                    self.log.info(imput.strip())
            
            if index == 5:
                timeouts = 0
                imput = self.p.before
                striped = imput.strip()
                if len(striped) > 0:
                    self.log.info(imput.strip())
        return output
            
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
        
        
        
    def logOutputSetEnv(self,fd,data,args,keys):
        #self.logOutput(fd,data,args,keys)
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
        
        lines = data.split('\n')
        for line in lines:
            if len(line) == 0:
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
                
            self.logOutput(fd,data,args,keys)
            
         
        
        
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
                if not line[:11] == "declare -x ":
                    # We only want declair lines
                    continue
                end = line[11:].split('="')
                if len(end) < 2:
                    continue
                
                tail = '="'.join(end[1:])
                head = end[0]
                
                self.FoundEnv[head] = tail[:-1]
            
            
        
    
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
        
        self.running.CbAddOnExit(self.ScriptOnExit)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptRunScriptStart = re.compile(startPrompt)
        self.promptRunScriptEnd = re.compile(endPrompt)
        self.waitingOnPromptRunScriptStart = True
        self.waitingOnPromptRunScriptEnd = False
        self.running.CbAddOnFdRead(self.logOutputRunScript)
        self.running.Write("echo %s\n" % (startPrompt))
        while self.waitingOnPromptRunScriptStart == True:
            self.running.Comunicate(timeout = 1)
        
        fp = open(script)
        for line in fp:
            cleanline = line.strip()
            self.log.info("run+%s" %(cleanline))
            self.running.Write(line)
        self.running.Write("echo %s\n" % (endPrompt))
        while self.waitingOnPromptRunScriptEnd == True:
            self.running.Comunicate()
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
                self.log.info("d")
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
        self.FoundEnv = {}
        output = {}
        self.running.CbAddOnFdRead(self.logOutputGetEnv)
        startPrompt = prompts.GeneratePrompt()
        endPrompt = prompts.GeneratePrompt()
        self.promptGetEnvStart = re.compile(startPrompt)
        self.promptGetEnvEnd = re.compile(endPrompt)
        
        self.waitingOnPromptGetEnvStart = True
        self.waitingOnPromptGetEnvEnd = True
        self.running.Write("echo %s\n" % (startPrompt))
        while self.waitingOnPromptGetEnvStart == True:
            self.running.Comunicate()
        self.FoundEnv = {}
        self.running.Write("declare -x\n")
        self.running.Write("echo %s\n" % (endPrompt))
        while self.waitingOnPromptGetEnvEnd == True:
            self.running.Comunicate()
        self.running.CbDelOnFdRead(self.logOutputGetEnv)
        return self.FoundEnv
    def finalise(self):

        self.running.Write("exit 0\n")
