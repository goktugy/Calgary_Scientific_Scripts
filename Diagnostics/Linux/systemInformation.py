'''
Created on Apr 7, 2015

@author: goktug.yorulmaz
'''
import os
import time
import platform
import psutil
import commands


class systemInfo(object):
    '''
    This class will retrieve system information from the Operating System 
    '''
    
    operatingSystem=None   #Information about the version of the Operating System
    memory=None    #Information about the memory in place     
    runTime=None
    usedPorts=None
    systemLogFile="./logs/SystemInfo.log" 
    
 
 
    def bytes2human(self,n):                
        """
        This function is designed to convert a large number into 
        a human readable format. 
        :param: A large number
        :returns: Returns the large number converted into a human readable format.
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        
        return "%sB" % n
 
 
    def getTime(self):
        """
        This function is designed to convert a large number into 
        a human readable for 
        :param: No parameters taken.
        :returns: Returns the actual time.
        """
        
        today=time.strftime("%c")
        try:
            if os.path.exists(self.systemLogFile):
                os.remove(self.systemLogFile)
        except OSError:    
            print "Could not delete existing %s" %self.systemLogFile 
        
        try:
            f=open(self.systemLogFile,"a")
            f.write("Today is %s \n" %today)
        except IOError:
            print "Error: can\'t open file %s"%self.systemLogFile    
        finally:
            f.close()
               
    def getOperatingSystem(self):
        """
        This function uses the platform library to get the 
        Operating System name
        Machine Architecture
        Machine Name
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """
        try:
            f=open(self.systemLogFile,"a")
            f.write("Platform Distribution is %s \n" %str(platform.dist()))
            f.write("System is %s \n" %platform.system())
            f.write("Machine Architecture is %s \n" %platform.machine())
            f.write('Machine Name is %s \n' %str(platform.uname()))
        except IOError:
            print "Error: can\'t open file %s \n"%self.systemLogFile    
        finally:
            f.close()
   
    def getMemory(self):
        """
        This function uses the psutil library to get the 
        Total memory
        Available memory
        Percentage memory
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """
        
        virtualMemory=psutil.virtual_memory()
        try:
            f=open(self.systemLogFile,"a")
            f.write("Total memory is %s \n" % self.bytes2human(virtualMemory[0]))
            f.write("Available memory is %s \n" %self.bytes2human(virtualMemory[1]))
            f.write("Percentage memory in use %s \n" % virtualMemory[2])
        except IOError:
            print "Error: can\'t open file %s \n"%self.systemLogFile    
        finally:
            f.close()
       
    def getSwapMemory(self):
        """
        This function uses the psutil library to get the 
        Total SWAP memory
        Used SWAP memory
        Free SWAP memory
        Percentage SWAP memory in use        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """
        
        swapMemory=psutil.swap_memory()
        try:
            f=open(self.systemLogFile,"a")
            f.write("Total SWAP memory is %s \n" % self.bytes2human(swapMemory[0]))
            f.write("Used SWAP memory is %s \n" %self.bytes2human(swapMemory[1]))
            f.write("Free SWAP memory is %s \n" % self.bytes2human(swapMemory[2]))
            f.write("Percentage SWAP memory in use is %s \n" % swapMemory[3])
        except IOError:
            print "Error: can\'t open file %s \n"%self.systemLogFile    
        finally:
            f.close()
    
    
    def getInstalledSoftware(self):
        """
        This function uses the rpm library to retrieve the list of installed software.
        In specific it queries for the following installed packages: "pureweb*","xorg-x11-fonts*","jdk","*gcj* 
        This is a platform specific information.
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """        
        try:
            f=open(self.systemLogFile,"a")
            f.write("\nCurrently the following software is installed \n")
        
            if( platform.system()=="Linux"):
                import rpm
                ts = rpm.TransactionSet()
                packagesList=["pureweb*","xorg-x11-fonts*","jdk","*gcj*"]
            
                for packageItem in packagesList:
                    mi = ts.dbMatch()
                    mi.pattern('name', rpm.RPMMIRE_GLOB, packageItem)
                    for h in mi:
                        f.write("%s-%s-%s \n"% (h['name'], h['version'], h['release']))  
        except IOError:
            print "Error: can\'t open file %s \n"%self.systemLogFile    
        finally:
            f.close()
    
     
    def getUsers(self):
        """
        This function uses the rpm library to retrieve the list of installed software.
        In specific it queries for the following installed packages: "pureweb*","xorg-x11-fonts*","jdk","*gcj* 
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """      
        try:
            userList=psutil.get_users()
            f=open(self.systemLogFile,"a")
            f.write("\nCurrently logged users are: \n")
             
            for user in userList:
                f.write("User name is %s \n" % user[0]) 
                f.write("User host is %s \n" %user[2])
                f.write("User logged at %s \n"%str(time.ctime(user[3])) )
                            
        except IOError:
            print "Error: can\'t open file %s \n"%self.systemLogFile    
        finally:
            f.close()
    
    
    def getRunTime(self):
        """
        This function uses the psutil library to retrieve the IP address of the machine.
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """  
        try:
            f=open(self.systemLogFile,"a")
            f.write("\nThe system booted at %s" % time.ctime(psutil.BOOT_TIME))
        except IOError:
                print "Error: can\'t open file %s \n"%self.systemLogFile    
        
        finally:
                f.close()
    
    def getJavaVersion(self):
        """
        This function uses the psutil library to get the java version of the machine.
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """  
        if( platform.system()=="Linux"):
            javaVersion=commands.getoutput("java -version")
            
            try:
                f=open(self.systemLogFile,"a")
                f.write("\n\nThe following java version is installed: %s"% javaVersion)               
        
            except IOError:
                print "Error: can\'t open file %s \n"%self.systemLogFile    
        
            finally:
                f.close()
    
    def getDeamons(self):
        """
        This function uses the commands library to get the list of processes.
        This is a platform dependent function
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """  
        if(platform.system()=="Linux"):
            deamonsList=commands.getoutput("ps aux")
            try:
                f=open(self.systemLogFile,"a")
                f.write("\n\nThe following deamons are running \n%s" % deamonsList)             
            except IOError:
                print "Error: can\'t open file %s \n"%self.systemLogFile    
        
            finally:
                f.close()
        
    def __init__(self):
        self.getTime()
        self.getOperatingSystem()
        self.getMemory()
        self.getSwapMemory()
        self.getInstalledSoftware()
        self.getUsers()
        self.getRunTime()
        self.getDeamons()
        self.getJavaVersion()
      
        