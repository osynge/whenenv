import json
import os
import logging


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
        # Grab all properties not already defined
        newdict = dict(holderBase.dictionary)
        updatedDict = newdict.update(self.dictionary)
        self.dictionary = updatedDict
        
        
    def getProvides(self):
        if u'provides' in self.dictionary.keys():
            value = self.dictionary["provides"]
            print value
            if isinstance(value, basestring):
                value = [value]
                
            return list(value)
        return []




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
    def addFromHolder(self,holder):
        holderName = holder.getName()
        if holderName == None:
            return False
        if holder.isComplete() != True:
            return False
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
        print 'ssss',self.allcontianed.keys()
        provides = {}
        inherits = set([])
        for item in available:
            if "inherits" in self.allcontianed[item].dictionary.keys():
                inherits.add(item)
            provideList = self.allcontianed[item].getProvides()
            print provideList
            for value in provideList:
                self.log.error("value=%s:%s" % (value, item))
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
            self.log.error("here")
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
            print lenInheritsLastPass
            # Now the loop safty is done we can get on fixinf inherited items
            for inheritor in set(inherits):
                inheritasnceList = list(self.allcontianed[inheritor].dictionary["inherits"])
                inheritasnceSet = set(inheritasnceList)
                if inheritor in inheritasnceSet:
                    self.log.error("Undefined inheritance:'%s':'%s'" % (inheritor,undefined))
                    continue
                undefined = complete.difference(inheritasnceSet)
                if len(undefined) != 0:
                    self.log.error("Undefined inheritance:'%s':'%s'" % (inheritor,undefined))
                    continue
                completeInherits = available.difference()
                print completeInherits
                missinginheritance = inheritasnceSet.difference(available)
                if len(missinginheritance) != 0:
                    self.log.error("missinginheritance:%s" % (len(missinginheritance)))
                    continue
                for ancestor in inheritasnceList:
                    if not item in completeInherits:
                        self.log.error("missingItem:%s" % (item))
                        continue
                    self.allcontianed[inheritor].inheritProperties(ancestor)
                print "here:"
                del self.allcontianed[item].dictionary["inherits"]
                inherits.remove(item)
                complete.add(item)
                
            
        if len(inherits) > 0:
            self.log.error("Invalid Inheritance:%s" % (inherits))
            
        
        self.provides = provides
        print "dddd",self.provides
            
        
        
        
    
class containerJobs(containerBase):
    def __init__(self, *args, **kwargs):
        super(containerJobs, self).__init__(*args, **kwargs)
        self.log = logging.getLogger("containerJobs")
    def addFromDictionary(self,JobAsDictionary):
        detailts = holderJob(JobAsDictionary)
        return self.addFromHolder(detailts)
    
    def Index(self):
        super(containerJobs, self).Index()
        
        
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
        
    

class matrixRunner(object):

    def __init__(self, *args, **kwargs):
        dirEnviroments = kwargs.get('dirEnviroments', None)
        dirJobs = kwargs.get('dirJobs', None)
        self.jobs = loaderJobs(cfgDir=dirJobs)
        self.enviroment = loaderEnviroment(cfgDir=dirEnviroments)
        self.log = logging.getLogger("matrixRunner")
        
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
