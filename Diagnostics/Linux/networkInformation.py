'''
Created on Apr 16, 2015

@author: goktug.yorulmaz
'''

import commands
import platform
import psutil

class networkInfo(object):
    '''
    This class will retrieve and store information about the network.
    '''
    networkingLogFile="./logs/NetworkInfo.log" 

    def getOpenPorts(self):
        """
        This function uses the commands library to get the list of open ports
        
        This is a platform dependent function
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file NetworkInfo.log.
        """  
        
        if(platform.system()=="Linux"):
            networkPorts=commands.getoutput("netstat -nap")
            try:
                f=open(self.networkingLogFile,"a")
                f.write("\nThe following ports are in use:\n%s" %networkPorts)
                                           
            except IOError:
                print "Error: can\'t open file %s \n"%self.networkingLogFile    
        
            finally:
                f.close()
     
     
    def getDNSInfo(self):
        """
        This function uses the commands library to get the DNS information.
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file NetworkInfo.log.
        """  
        
        
        if(platform.system()=="Linux"):
            DNS=commands.getoutput("cat /etc/resolv.conf")
            try:
                f=open(self.networkingLogFile,"a")
                f.write("\n\nThe following DNS information is available:\n%s" %DNS)
                                           
            except IOError:
                print "Error: can\'t open file %s \n"%self.networkingLogFile    
        
            finally:
                f.close()
                
    def getNetworkHealth(self):
        
        """
        This function uses the psutil library to get network health settings:
        The number of bytes sent
        The number of bytes received
        The number of packets sent
        The number of packets received
        The number of errors while receiving
        The number of errors while sending
        The number of packets dropped while receiving
        The number of packets dropped while sending
        
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file NetworkInfo.log.
        """  
        
        
        networkStats=psutil.network_io_counters()
        try:
                f=open(self.networkingLogFile,"a")
                f.write("\n\nThe following network health diagnostics is available: ")
                f.write("\nThe number of bytes sent: %s" %networkStats[0])
                f.write("\nThe number of bytes received: %s" %networkStats[1])
                f.write("\nThe number of packets sent: %s" %networkStats[2])
                f.write("\nThe number of packets received: %s" %networkStats[3])  
                f.write("\nThe number of errors while receiving: %s" %networkStats[4])
                f.write("\nThe number of errors while sending: %s" %networkStats[5])
                f.write("\nThe number of packets dropped while receiving: %s" %networkStats[6])
                f.write("\nThe number of packets dropped while sending: %s" %networkStats[7])                                                         
        
        except IOError:
                print "Error: can\'t open file %s \n"%self.networkingLogFile    
        
        finally:
                f.close()


    def getIPAddress(self):
        """
        This function uses the commands library to retrieve the IP address of the machine.
        This is a platform dependent function.
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """  
        
        if( platform.system()=="Linux"):
            ipAddress=commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
            try:
                f=open(self.networkingLogFile,"w")
                f.write("The IP address of the machine is %s" % ipAddress)
             
            except IOError:
                print "Error: can\'t open file %s \n"%self.networkingLogFile    
        
            finally:
                f.close()
                
                
    def getHosts(self):
        """
        This function uses the commands library to retrieve the IP address of the machine.
        This is a platform dependent function
        :param: No parameters taken.
        :returns: Writes the retrieved information to the log file SystemInfo.log.
        """  
        
        if( platform.system()=="Linux"):
            hostsList=commands.getoutput("more /etc/hosts").split("\n")
            try:
                f=open(self.networkingLogFile,"a")
                f.write("\n\nThe following hosts are specified in /etc/hosts file:")
                for host in hostsList:
                    f.write("\nThe following host is specified: %s" %host)
             
            except IOError:
                print "Error: can\'t open file %s \n"%self.networkingLogFile    
        
            finally:
                f.close()            
                
                
     
    def __init__(self):
        self.getIPAddress()
        self.getOpenPorts()
        self.getDNSInfo()
        self.getNetworkHealth()
        self.getHosts()