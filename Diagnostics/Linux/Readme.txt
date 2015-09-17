Overview
----------
The script is designed to get system diagnostics about Linux/CentOS Operating System.
The script will also run on Windows platform however it will not gather as much information.
It will also get information about ResolutionMD/PureWeb if they are installed.

How to run the script?
-----------------------
To run the scripts you need to install

-python-psutil.0.6.1-1.el6.x64_64.rpm

This rpm contains the psutil python library that is necessary to run this python script.

To install the library type:

rpm -ivh python-psutil.0.6.1-1.el6.x64_64.rpm

Once the psutil library has been installed you may need to execute 

chmod +x *.py (This is to enable execution permissions on python files)

in order to execute the scripts.

To run the script type at the command: python ./Diagnostics.py

As the script starts running it will prompt you: 

"Welcome to Linux Diagnostics Script"
"The script will gather diagnostics information about your system"
"The script will also gather information about ResolutionMD"

and execute in the background.

Understanding The Results
--------------------------
The script will produce the following .log files in the logs folder.

SystemInfo.log --> Information about the system
HardwareInfo.log--> Information about the hardware in place
NetworkInfo.log --> Information about the network setup
KernelInfo.log --> Graphics cards/driver messages from the kernel 

In addition it will create a zip file by the name of logs.zip 
that will contain all the log files.
