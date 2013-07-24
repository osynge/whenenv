import json
import os
import logging
import chroot_script_runner
import observable
class holderBase(object):
    def __init__(self, dictionary,*args, **kwargs):
        self.log = logging.getLogger("holderBase")
        self.requiredKeysBase = set(["name"])
        self.dictionary = dictionary
    def getName(self):
        if u'name' in self.dictionary.keys():
            return self.dictionary["name"]
        self.log.error("missing name")
        return None
    def getInheritance(self):
        if u'inherits' in self.dictionary.keys():
            return list(self.dictionary["inherits"])
        return []
            
    def isComplete(self):
        missignKeys = self.requiredKeysBase.difference(self.dictionary.keys())
        if len(missignKeys) > 0:
            self.log.error("missing keys %s" % (missignKeys))
            return False
        return True
    
    def inheritProperties(self,holderBase):
        #self.log.error("inheritProperties,%s,%s" % (self.getName(),holderBase.getName()))
        # Grab all properties not already defined
        newdict = dict(holderBase.dictionary)
        newdict.update(self.dictionary)
        self.dictionary = newdict
        
        
    def getProvides(self):
        if u'provides' in self.dictionary.keys():
            value = self.dictionary["provides"]
            #print value
            if isinstance(value, basestring):
                value = [value]
                
            return list(value)
        return []
    
    
    def getDepends(self):
        if u'depends' in self.dictionary.keys():
            value = self.dictionary["depends"]
            #print value
            if isinstance(value, basestring):
                value = [value]
                
            return list(value)
        return []
    def getVariablesProvided(self):
        if not u'variables' in self.dictionary.keys():
            return []
        if not 'provides_keys' in self.dictionary[u'variables'].keys():
            return []
        return list(self.dictionary[u'variables']['provides_keys'])
    
    def matchesVariablesValue(self,enviroment):
        if not u'variables' in self.dictionary.keys():
            self.log.error("no variables set for %s" % (self.getName()))
            return False
        if 'require_values' in self.dictionary[u'variables'].keys():
            required = self.dictionary[u'variables']['require_values']
            envKeys = set(enviroment.keys())
            for key in required.keys():
                if not key in envKeys:
                    return False
                if required[key] != enviroment[key]:
                    return False
        return True
        
    def matchesVariablesProvided(self,VariablesProvided):
        if not u'variables' in self.dictionary.keys():
            self.log.error("no variables set for %s" % (self.getName()))
            return False
        if 'require_keys' in self.dictionary[u'variables'].keys():
            #print VariablesProvided,self.dictionary[u'variables']['require_keys']
            #print VariablesProvided.issuperset(self.dictionary[u'variables']['require_keys'])
            return set(VariablesProvided).issuperset(self.dictionary[u'variables']['require_keys'])
        return True

class holderJob(holderBase):
    def __init__(self, dictionary, *args, **kwargs):
        super(holderJob, self).__init__(dictionary, *args, **kwargs)
        self.log = logging.getLogger("holderJob")
        self.requiredKeysBase = self.requiredKeysBase.union(["enviroment"])
    

class holderEnviroment(holderBase):
    def __init__(self, dictionary, *args, **kwargs):
        super(holderEnviroment, self).__init__(dictionary, *args, **kwargs)
        self.log = logging.getLogger("holderEnviroment")
        self.requiredKeysBase = self.requiredKeysBase.union(["lifecycle"])
    

        


class containerBase(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("containerBase")
        self.cfgDir = kwargs.get('dirJobs', None)
        self.allcontianed = {}
        self.provides = {}
        
    def addFromHolder(self,holder):
        holderName = holder.getName()
        if holderName == None:
            return False
        allHolderNames = self.allcontianed.keys()
        if holderName in allHolderNames:
            self.log = logging.getLogger("over writing %s" % (holderName))
        self.allcontianed[holderName] = holder
        return True
        
    def addFromDictionary(self,JobAsDictionary):
        print 'shoudl not be here'
    
    def ListAvailable(self):
        return self.allcontianed.keys()
    
    
    def Index(self):
        # Should be called aftert each block l
        # of items added to the dictionary
        available = set(self.allcontianed.keys())
        provides = {}
        inherits = set([])
        for item in available:
            inheritsList = self.allcontianed[item].getInheritance()
            if len(inheritsList) > 0:
                inherits.add(item)
            provideList = self.allcontianed[item].getProvides()
            for value in provideList:
                #self.log.error("value=%s:%s" % (value, item))
                if value in provides.keys():
                    provides[value].append(item)
                else:
                    provides[value] = [item]

                
        complete =  available.difference(inherits)
        lenInherits = len(inherits)
        InheritsPass = 0
        lenInheritsLastPass = lenInherits + 2
        #print  InheritsPass < lenInherits
        #self.log.error("InheritsPass=%s:%s" % (InheritsPass, lenInherits))
        while InheritsPass < lenInherits:
            InheritsPass += 1
            lenInherits = len(inherits)
            if InheritsPass > lenInherits:
                # Inherits tree max deapth found
                self.log.error("max repeat")
                break
            if lenInheritsLastPass == lenInherits:
                # We are not resolving the inherits tree further.
                self.log.error("unresolved inherits")
                break
            lenInheritsLastPass = lenInherits
            #print lenInheritsLastPass
            # Now the loop safty is done we can get on fixinf inherited items
            for inheritor in set(inherits):
                if not inheritor in inherits:
                    continue
                inheritasnceList = list(self.allcontianed[inheritor].dictionary["inherits"])
                inheritasnceSet = set(inheritasnceList)
                if inheritor in inheritasnceSet:
                    self.log.info("Undefined removed inheritance:'%s':'%s'" % (inheritor,inheritasnceList))
                    continue
                undefined = inheritasnceSet.difference(complete)
                if len(undefined) != 0:
                    self.log.error("Undefined inheritance:'%s':'%s'" % (inheritor,undefined))
                    continue
                completeInherits = available.difference()
                missinginheritance = inheritasnceSet.difference(available)
                if len(missinginheritance) != 0:
                    self.log.error("missinginheritance:%s" % (len(missinginheritance)))
                    continue
                for ancestor in inheritasnceList:
                    if not item in completeInherits:
                        self.log.error("missingItem:%s" % (item))
                        continue
                    
                    self.allcontianed[inheritor].inheritProperties(self.allcontianed[ancestor])
                    #self.log.error("allcontianed[%s] = %s" % (inheritor,ancestor))
                if "inherits" in self.allcontianed[item].dictionary.keys():
                    del self.allcontianed[item].dictionary["inherits"]
                inherits.remove(inheritor)
                complete.add(inheritor)

        if len(inherits) > 0:
            self.log.error("Invalid Inheritance:%s" % (inherits))
            for item in inherits:
                self.log.info("item=%s:%s" % (item,self.allcontianed[item].dictionary))
            #for item in available:
            #    self.log.info("availableitem=%s:%s" % (item,self.allcontianed[item].dictionary))
        
        self.provides = provides
        self.log.info("provided=%s" % (self.provides.keys()))
            
    def listJobsProvide(self,filer):
        #self.log.error("getJobsPlan")
        if not filer in self.provides.keys():
            return []
        return self.provides[filer]
        
    
class containerJobs(containerBase):
    def __init__(self, *args, **kwargs):
        super(containerJobs, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("containerJobs")
    def addFromDictionary(self,JobAsDictionary):
        detailts = holderJob(JobAsDictionary)
        return self.addFromHolder(detailts)
    
    def Index(self):
        super(containerJobs, self).Index()

    
    def getJobs(self,enviroment,requirement):
        possiblePlans = self.listJobsProvide(requirement)
        matches = []
        for plan in possiblePlans:
            testEnv = dict(enviroment)
            testKeys = set(testEnv.keys())
            if True != self.allcontianed[plan].matchesVariablesProvided(testKeys):
                #self.log.error("matchesVariablesProvided=%s" % (testKeys))
                continue
            if True != self.allcontianed[plan].matchesVariablesValue(testEnv):
                #self.log.error("matchesVariablesValue=%s" % (testKeys))
                continue
            matches.append(plan)
        lenMatchesKey = len(matches) 
        if lenMatchesKey == 0:
            self.log.error("No matching jobs for '%s' with %s" % (requirement,enviroment))
            return []
        if lenMatchesKey == 1:
            return matches
        if lenMatchesKey > 1:
            self.log.error("Too many matches for jobs for '%s' with %s %s" % (requirement,requirement,matches))
            return []
        self.log.error("Programming error with matches for jobs for '%s' with %s" % (requirement,requirement))
        return []
    def getRequire(self,name):
        return self.allcontianed[name].getDepends()
        
class containerEnviroment(containerBase):
    def __init__(self, *args, **kwargs):
        super(containerEnviroment, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("containerEnviroment")
    def addFromDictionary(self,JobAsDictionary):
        detailts = holderEnviroment(JobAsDictionary)
        return self.addFromHolder(detailts)
 
class loaderBase(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("loaderBase")
        self.cfgDir = kwargs.get('cfgDir', None)
        self.cfgContainer = containerBase(dirJobs=self.cfgDir)
    def load(self):
        knownFiles = []
        if self.cfgDir == None:
            self.log.error("cfgDir=None")
            return False
        for root, dirs, files in os.walk(self.cfgDir):
            for fileName in files:
                filepath = "%s%s" % (root , fileName)
                knownFiles.append(filepath)
        for CfgFile in knownFiles:
            if not os.path.isfile(CfgFile):
                continue
            fp = open(CfgFile)
            try:
                parsedJson = json.load(fp)
            except ValueError,E:
                self.log.error("InvalidJson:%s:%s" % (E,CfgFile))
                continue
            self.cfgContainer.addFromDictionary(parsedJson)
        self.cfgContainer.Index()
        return True  

class loaderEnviroment(loaderBase):
    def __init__(self, *args, **kwargs):
        super(loaderEnviroment, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("loaderEnviroment")
        self.cfgContainer = containerEnviroment(dirJobs=self.cfgDir)
        


class loaderJobs(loaderBase):
    def __init__(self, *args, **kwargs):
        super(loaderJobs, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("loaderJobs")
        self.cfgContainer = containerJobs(dirJobs=self.cfgDir)
    
    
    def getJobs(self,enviroment,requirement):
        possiblePlans = self.cfgContainer.listJobsProvide("execution")
        matches = []
        for plan in possiblePlans:
            testEnv = dict(enviroment)
            testKeys = set(testEnv.keys())
            if True != self.cfgContainer.allcontianed[plan].matchesVariablesProvided(testKeys):
                continue
            if True != self.cfgContainer.allcontianed[plan].matchesVariablesValue(testEnv):
                continue
        lenMatchesKey = len(matches.keys())
        if lenMatchesKey == 0:
            self.log.error("No matching jobs for '%s' with %s" % (requirement,requirement))
            return []
        if lenMatchesKey == 1:
            return matches
        if lenMatchesKey > 1:
            self.log.error("Too many matches for jobs for '%s' with %s" % (requirement,requirement))
            return []
        self.log.error("Programming error with matches for jobs for '%s' with %s" % (requirement,requirement))
        return []
    def getJobsPlan(self,enviroment):
        # replace thsi code with soem thign better later
        # using a dependacy stack processor and comparing 
        # variabels on the go.
        self.log.error("getJobsPlan=%s" % (enviroment))
        # Now we test the plans
        tree = {}
        possiblePlans = self.cfgContainer.listJobsProvide("execution")
        for plan in possiblePlans:
            testEnv = dict(enviroment)
            testKeys = set(testEnv.keys())
            if True != self.cfgContainer.allcontianed[plan].matchesVariablesProvided(testKeys):
                self.log.error("matchesVariablesProvided=%s" % (testKeys))
                continue
            
            if True != self.cfgContainer.allcontianed[plan].matchesVariablesValue(testEnv):
                self.log.error("matchesVariablesValue=%s" % (testKeys))
                continue
            tree[plan] = [plan]
        resolutionStack = {}
        dependacyStack = {}
        if len(tree.keys()) == 0:
            self.log.error("No matching jobs for")
            return []
        for key in tree.keys():
            DoneJob = set()
            DoneStack = set()
            dependacyList =  key
            depStack = []
            JobStack = [key]
            
            self.log.error("JobStack=%s" % (JobStack))
            self.log.error("depStack=%s" % (depStack))
            
            shouldRun = True
            while shouldRun == True:
                if len(JobStack) + len(depStack) == 0:
                    shouldRun = False
                    continue
                JobNext = None
                if len(JobStack) > 0:
                    self.log.error("JobStack=%s" % (JobStack))
                    tmpCommand = JobStack.pop(0)
                    self.log.debug("JobStack=%s" % (JobStack))
                    self.log.debug("tmpCommand=%s" % (tmpCommand))
                    if not tmpCommand in DoneJob:
                        JobNext = tmpCommand
                        DoneJob.add(tmpCommand)
                nextDepends = None 
                if len(depStack) > 0:
                    tmpStack = depStack.pop(0)
                    if not tmpStack in DoneStack:
                        nextDepends = tmpStack
                        DoneStack.add(tmpStack)

                if nextDepends != None:
                    self.log.debug("nextDepends=%s" % (nextDepends))
                    matchinJobs = []
                    possibleJobs = self.cfgContainer.listJobsProvide(nextDepends)
                    for job in possibleJobs:
                        #self.log.error("job=%s=%s" % ())
                        matchinJobs.append(job)
                        JobStack.append(job)
                    resolutionStack[nextDepends] = possibleJobs
                    
                 
                if JobNext != None:
                    self.log.debug("JobNext=%s" % (JobNext))   
                    depends = self.cfgContainer.allcontianed[JobNext].getDepends()
                    self.log.debug("depends=%s" % (depends))   
                    
                    for item in depends:
                        if item in depStack:
                            continue
                        self.log.error("item=%s" % (item))
                        depStack.append(item)
                    if JobNext in dependacyStack.keys():
                        dependacyStack[JobNext] = depends.union(dependacyStack[JobNext])
                    else:
                        dependacyStack[JobNext] = depends
        
        # now we have the dpeendacy tree
        # We can try to pass it:
        #self.log.error("dependacyStack=%s" % (dependacyStack))  
        #self.log.error("resolutionStack=%s" % (resolutionStack))  
        unifiedTree = {}
        for key in tree.keys():
            stack = [key]
            matching = dependacyStack.keys()
            if not key in matching:
                self.log.error("key not found=%s" % (key))  
                continue
            testEnv = dict(enviroment)
            depStack = dependacyStack[key]
            possibleFirstJob = []
            for item in depStack:
                joblist = resolutionStack[item]
                cleanProvided = []
                nosolutions = False
                for job in joblist:
                    matchesVariablesValue = self.cfgContainer.allcontianed[job].matchesVariablesValue(testEnv)
                    if matchesVariablesValue == True:
                        cleanProvided.append(job)
                if len(cleanProvided) == 0:
                    self.log.error("No solutions to %s" %(job))
                    possibleFirstJob.append(None)
                    continue
                if len(cleanProvided) > 1:
                    self.log.error("to many solutions both %s" % (cleanProvided))
                    continue
                possibleFirstJob.append(cleanProvided[0])
                
            unifiedTree[key] = possibleFirstJob
        badkeys = []
        for key in unifiedTree.keys():
            vesult = unifiedTree[key]
            if None in vesult:
                badkeys.append(key)
        for key in badkeys:
            self.log.error("Skipping %s : %s" %(key,unifiedTree))
            del unifiedTree[key]
        #self.log.error("unifiedTree %s" %(    unifiedTree))
        #self.log.error("dependacyStack=%s" % (dependacyStack))  
        #self.log.error("resolutionStack=%s" % (resolutionStack))  
        unifiedTreeKeyLen = len(unifiedTree.keys())
        if unifiedTreeKeyLen == 0:
            self.log.error("dependacyStack=%s" % (dependacyStack))
            self.log.error("resolutionStack=%s" % (resolutionStack))
            return []
        if unifiedTreeKeyLen > 1:
            self.log.error("to many solutions both %s" % (unifiedTree))
            return []
        value = None
        for key in unifiedTree.keys():
            value = unifiedTree[key] + [key]
        return value




matrixRequiresStateIdle = 0
matrixRequiresStateRunning = 1
matrixRequiresStateFinished = 2


class matrixRequiresStackPointer(object):
    def __init__(self, *args, **kwargs):
        self.enviroment = kwargs.get('enviroment', None)
        self.EnvContainer = kwargs.get('env_container', None)
        self.JobContainer = kwargs.get('job_container', None)
        self.ExecutionPonter = observable.Observable(None)
        self.ExecutionStatus = observable.Observable(matrixRequiresStateIdle)
        self.RequiresStack = []
        self.JobsDone = []
        self.log = logging.getLogger("matrixRequiresStackPointer")
        self.basedir = kwargs.get('basedir', None)
        
    def PushStack(self,requires):
        self.RequiresStack = [requires] + self.RequiresStack

    
    def runstage(self,item):
        self.log.info("Running Command '%s'" % (item))
        if not "script" in self.JobContainer.allcontianed[item].dictionary.keys():
            self.log.info("No script for Command '%s'" % (item))
            return 0
            
        self.JobContainer.allcontianed
        rs = chroot_script_runner.runnershell2(command="/bin/sh")
        rs.initialise()
        #self.log.info("Initisaalised Command '%s'" % (item))
        rs.setEnv(self.enviroment)
        #self.log.info("setEnv Command '%s'" % (self.enviroment))
        initialEnv = rs.getEnv()
        #self.log.info("getEnv Command '%s'" % (item))
        script = self.JobContainer.allcontianed[item].dictionary["script"]
        fullpath = "%s/%s" % (self.basedir , script)
        self.log.info("Running is script '%s'" % (script))
        self.log.info("Running is script '%s'" % (fullpath))
        
        output = rs.runscript(fullpath)
        if output != 0:
            self.log.error("Job Part '%s' failed with '%s'" % (script,output))
            return output
        
        finalEnv = rs.getEnv()
        initialKeys = set(initialEnv.keys())
        finalKeys = set(finalEnv.keys())
        newkeys = finalKeys.difference(initialKeys)
        for key in newkeys:
            
            self.enviroment[key] = finalEnv[key]
        return 0
            
    def getNextJob(self):
        if len(self.RequiresStack) == 0:
            self.info = logging.getLogger("No Requirestack")
            return 0

        needToExpandDeps = True
        firstJob = None
        while True:
            self.log.debug("Enviroment %s" % (self.enviroment))
            self.log.info("Stack %s '%s'" % (self.RequiresStack,self.JobsDone))
            
            if len(self.RequiresStack) == 0:
                self.info = logging.getLogger("No Requirestack")
                return 0
            matches = self.JobContainer.getJobs( self.enviroment ,self.RequiresStack[0])
            if len(matches) == 0:
                self.log = logging.getLogger("No matcvhes")
                return 1
            firstJob = matches[0]
            requires = self.JobContainer.getRequire(firstJob)
            if len(requires) > 0:
                requires.extend(self.RequiresStack)
                self.RequiresStack = requires
                continue
            # No dependacies
            if firstJob in self.JobsDone:
                del self.RequiresStack[0]
                continue
            rc = self.runstage(firstJob)
            if rc != 0:
                self.info = logging.getLogger("rc")
                return rc
            self.JobsDone.append(firstJob)
            del self.RequiresStack[0]
        
    def isFinished(self):
        # returns if the iterator will fail with None
        pass   
    def isDone(self):
        
        return True

class matrixRunner(object):

    def __init__(self, *args, **kwargs):
        dirEnviroments = kwargs.get('dirEnviroments', None)
        dirJobs = kwargs.get('dirJobs', None)
        self.jobs = loaderJobs(cfgDir=dirJobs)
        self.enviroment = loaderEnviroment(cfgDir=dirEnviroments)
        self.log = logging.getLogger("matrixRunner")
        self.log = logging.getLogger("matrixRunner")
        self.basedir = kwargs.get('basedir', None)
        
    def loadconfig(self):
        successLoadingJobs = self.jobs.load()
        if successLoadingJobs != True:
            self.log.error("Failed to load jobs")
            return False
        successLoadingEnviroment = self.enviroment.load()
        if successLoadingEnviroment != True:
            self.log.error("Failed to load enviroment")
            return False
        
        return True
    
    def Run(self,enviroment):
        RequiresStack = matrixRequiresStackPointer(job_container = self.jobs.cfgContainer,
            env_container = self.enviroment.cfgContainer,
            enviroment = enviroment,
            basedir = self.basedir)
        RequiresStack.PushStack("execution")
        self.log.info("Starting planless")
        ranOk = RequiresStack.getNextJob()
        return ranOk
    
