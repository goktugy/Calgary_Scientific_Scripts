'''
Created on Apr 7, 2015
@author: goktug.yorulmaz
'''
from systemInformation import systemInfo
from hardwareInformation import hardwareInfo
from networkInformation import networkInfo
import logging
import os
import platform
import commands

def Welcome():
    """
         This function presents the user with a welcome message
         to the program.
         The functions waits for the user to click on the Return key to execute the
         programs 
        :param: No parameters specified
        :returns: Continues with the rest of the execution.
    """
    print ("Welcome to Linux Diagnostics Script")
    print ("The script will gather diagnostics information about your system")
    print ("The script will also gather information about ResolutionMD")
    

def createZip():
    if(platform.system()=="Linux"):
        try:
            if(os.path.exists("./logs.zip")):
                os.remove("./logs.zip")
            
            commands.getoutput("zip logs.zip ./logs/*.*")
                    
        except:
            print "Error creating zip file"    
        


if __name__ == '__main__':
    
    if(not os.path.lexists("./logs")):
        os.makedirs("./logs")
    
    
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', 
                        filename='./logs/Diagnostics.log', 
                        level=logging.DEBUG, 
                        filemode='w')
    logging.debug('Started')
    Welcome()
    logging.debug('Creating logs directory')
    
   
    logging.debug('Getting Current System Info')
    currentSystem=systemInfo()
    logging.debug('Finished Getting Current System Info')
    logging.debug('Getting Current Hardware Information')
    currentHardware=hardwareInfo()
    logging.debug('Finished Getting Current Hardware Information')
    logging.debug('Getting Current Network Information')
    currentNetworking=networkInfo()
    logging.debug('Finished Getting Current Network Information')
    logging.debug('Creating a zip file')
    createZip()