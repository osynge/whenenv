import logging
import uuid
import base64
import pexpect
import string
transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )

class runnershell:
    def __init__(self, chrootCmd, env):
        self.log = logging.getLogger("runnershell")
        self.chrootCmd = chrootCmd
        match_prompt = uuid.uuid1()
        self.prompt = base64.b32encode(str(match_prompt).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        self.env = env
        self.p = None
    
    
    def setPrompt(self):
        self.p.flush()
        match_one =  uuid.uuid1()
        bashvar_one = base64.b32encode(str(match_one).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        match_two =  uuid.uuid1()
        bashvar_two = base64.b32encode(str(match_two).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
        
        sent = 'echo %s\n' % (bashvar_one)
        self.p.send(sent)
        index = self.p.expect ([bashvar_one,pexpect.EOF, pexpect.TIMEOUT],timeout=10)
        self.p.send("PS1=%s\n" % (self.prompt))
        self.p.send("export PS1\n")
        self.p.flush()
        
        
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
            self.p.wait()
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
            self.log.critical("index=%s" %(index))
            if index == 0:
                imput = self.p.before
                if len(imput) == 0:
                    continue
                self.log.info("dinggga=%s" % (imput))
                secondlevel = self.p.expect (['"\r\n',pexpect.EOF, pexpect.TIMEOUT],timeout=20)
                imput = self.p.before
                self.log.info("secondlevel=%s=%s" % (secondlevel,imput))
                if secondlevel == 0:
                    imput = self.p.before
                    striped = imput.strip()
                    if len (striped) == 0:
                        continue
                    #self.log.info("secondlevel=%s" % (striped))
                    splitline = striped.split('="')
                    self.log.info("splitline=%s" % (splitline))
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
            index = self.p.expect ([bashvar_one,self.prompt,pexpect.EOF, pexpect.TIMEOUT],timeout=5)
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
            
