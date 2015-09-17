'''
Created on Apr 10, 2015

@author: goktug.yorulmaz
'''

import psutil
import platform
import commands

class hardwareInfo(object):
    '''
    This class will retrieve and store all the information about hardware
    '''
    
    drivers=None;
    PhysicalSpace=None
    drivers=None
    hardwareLogFile="./logs/HardwareInfo.log" 
    graphicCardsCount=0
    kernelLogFile="./logs/KernelInfo.log"

    def bytes2human(self,n):
        """
        This method is designed to convert a large number into 
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

    def getPartitions(self):
        
        """
        This method is designed to retrieve the hard disk partitions information
        using the psutil library. It provides:
        
        -Hard Disk Size
        -Used Space
        -Available Free Space
        -Percentage Use
        -Hard Disk Type
        -Mount Information
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        
        templ = "%35s %8s %8s %8s %5s%% %9s %s \n"
        
        try:
            f=open(self.hardwareLogFile,"w")
            f.write("The following partitions are in place: \n\n")
            f.write(templ  % ("Device", "Total", "Used", "Free", "Use ", "Type","Mount"))
        
            for part in psutil.disk_partitions(all=False):
                usage = psutil.disk_usage(part.mountpoint)
                f.write(templ % (
                             part.device,
                             self.bytes2human(usage.total),
                             self.bytes2human(usage.used),
                             self.bytes2human(usage.free),
                             int(usage.percent),
                             part.fstype,
                             part.mountpoint))
        except IOError:
                print "Error: can\'t open file %s \n"%self.hardwareLogFile    
        
        finally:
                f.close()
  
     
    def getCPU(self):
        
        """
        This method is designed to retrieve the cpu information
        using the psutil library. It provides
        
        -CPU Time spent in user mode
        -CPU Time spent in user mode with low priority
        -CPU Time spent in system mode in seconds
        -CPU Time spent in idle mode in seconds
        -CPU Total Time
        -CPU Percentage Usage
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        cpu=psutil.cpu_times()
        
        try:
            f=open(self.hardwareLogFile,"a")
            f.write("\nCPU Information\n")
            f.write("CPU Time spent in user mode in seconds is : %s \n" % cpu.user)
            f.write("CPU Time spent in user mode with low priority in seconds is : %s \n" %cpu[1])
            f.write("CPU Time spent in system mode in seconds is: %s \n" % cpu.system)
            f.write("CPU Time spent in idle mode in seconds is: %s \n" %cpu.idle)
            cpuTimeUsed= cpu.user + cpu.system + cpu[1]
            f.write("CPU Time Used in seconds is : %s\n" % (cpuTimeUsed))
            cpuTimeTotal=cpuTimeUsed+cpu.idle
            f.write("CPU Total Time is : %s \n" % (cpuTimeTotal))
            f.write("CPU Usage has been : %f percent \n" % ((cpuTimeUsed/cpuTimeTotal)*100) )
            
        except IOError:
            print "Error: can\'t open file %s \n" %self.hardwareLogFile    
    
        finally:
                f.close()
  
    def getGraphicsCard(self):
        
        """
        This method is designed to retrieve Graphics Card information
        using the commands library. It provides
        
        -The number of graphics cards
        -The type of graphics cards
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        if(platform.system()=="Linux"):
            graphicsCardInfo=commands.getoutput("/sbin/lspci | grep VGA")
            try:
                f=open(self.hardwareLogFile,"a")
                self.graphicCardsCount= len(graphicsCardInfo.split("\n"))
                f.write("\nThere are %s graphics cards "%str(self.graphicCardsCount))
                f.write("\nThe graphic cards are the following :\n%s" %graphicsCardInfo)
                
                           
            except IOError:
                print "Error: can\'t open file %s \n"%self.hardwareLogFile    
        
            finally:
                f.close()
    
    
    
    def getGraphicsCardDrivers(self):
         
        """
        This method is designed to retrieve Graphics Card driver information
        using the commands library. It provides
        
        -Graphics card driver version.
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        
        if(platform.system()=="Linux"):
            graphicsCardDrivers=commands.getoutput("cat /proc/driver/nvidia/version")
            try:
                f=open(self.hardwareLogFile,"a")
                f.write("\n\nThe graphic card drivers is the following :\n%s" %graphicsCardDrivers)
             
            except IOError:
                print "Error: can\'t open file %s \n"%self.hardwareLogFile    
        
            finally:
                f.close()
    
    
    def getXorgConfiguration(self): 
        
        """
        This method is designed to retrieve Xorg configuration information
        using the commands library. It provides
        
        -Xorg configuration settings.
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        if(platform.system()=="Linux"):
            xorgConfiguration=commands.getoutput("cat /etc/X11/xorg.conf")
            try:
                f=open(self.hardwareLogFile,"a")
                f.write("\n\nThe xorg Configuration is the following :\n%s" %xorgConfiguration)
             
            except IOError:
                print "Error: can\'t open file %s \n"%self.systemLogFile    
        
            finally:
                f.close()
    
    def getXorgLog(self):
        
        """
        This method is designed to retrieve Xorg configuration information
        using the commands library. It provides
        
        -Xorg configuration settings.
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        
        if(platform.system()=="Linux"):
            xorgLog=commands.getoutput("cat /var/log/Xorg.0.log")
            
            try:
                f=open(self.hardwareLogFile,"a")
                f.write("\n\nThe xorg log contains the following :\n%s" %xorgLog)
             
            except IOError:
                print "Error: can\'t open file %s \n"%self.hardwareLogFile    
        
            finally:
                f.close()
    
    def openGLInfo(self):
         
        """
        This method is designed to retrieve Xorg configuration information
        using the commands library. It provides
        
        -Xorg configuration settings.
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """
        
        if(platform.system()=="Linux"):
            
            try:
                f=open(self.hardwareLogFile,"a")
                for index in range(self.graphicCardsCount):
                    openGLInfo=commands.getoutput("glxinfo -display :0."+str(index)+" 2>&1 | grep -i 'direct' ")
                    f.write("\n\nThe system contains the following openGL information for graphics card %s:\n %s" %(index, openGLInfo))
             
            except IOError:
                    print "Error: can\'t open file %s \n"%self.hardwareLogFile    
        
            finally:    
                f.close() 
    
    
    def getKernelMessages(self):
        """
        This method is designed to retrieve kernel messages related to nvidia drivers
        and graphics card using the commands library. 
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file KernelInfo.log.
        
        """
        
        if(platform.system()=="Linux"):
            kernelMessages=commands.getoutput("dmesg | grep -iC 4 nvidia")
            try:
                f=open(self.kernelLogFile,"w")
                f.write("The following kernel messages have been reported with respect to the graphics card\n\n%s" %kernelMessages)
            except IOError:
                print "Error: can\'t open file %s \n"%self.kernelLogFile 
            finally:
                f.close()          
    
    def getNvidiaSnapShot(self):
        """
        This method is designed to retrieve a health check snapshot of the nvidia graphics card
        using the commands library. 
        
        This method is platform dependent.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file HardwareInfo.log.
        
        """        
        if(platform.system()=="Linux"):
            nvidiaSnapshot=commands.getoutput("nvidia-smi")
            try:
                f=open(self.hardwareLogFile,"a")
                f.write("\n\nThe following nvidia snapshot is available: \n%s" % nvidiaSnapshot)
            except IOError:
                print "Error: can\'t open file %s \n"%self.hardwareLogFile 
            finally:
                f.close()       
    
      
    def __init__(self):
        self.getPartitions()
        self.getCPU()
        self.getGraphicsCard()
        self.getGraphicsCardDrivers()
        self.getXorgConfiguration()
        self.getXorgLog()
        self.openGLInfo()
        self.getKernelMessages()
        self.getNvidiaSnapShot()
        