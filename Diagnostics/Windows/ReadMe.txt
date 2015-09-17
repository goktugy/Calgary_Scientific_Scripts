How to run the script?
-----------------------
In order to run the script you need to start Powershell (Go to Start Menu type Powershell on the Search)
as an administrator. (After you have found a Powershell listing right click and choose to launch it as an administrator)
When searching for Powershell you may see the following listings:

-Windows PowerShell
-Windows PowerShell (x86)

Windows PowerShell is the 64 bit version and Windows PowerShell (x86) is the 32 bit. 
You can select either one of them and it should work fine.
However make sure you start Powershell with Administrator privileges.

Once you start Powershell we need to enable the execution of Powershell scripts. 
First lets find out what Powershell execution policy you have in place.

Type Get-ExecutionPolicy at the Powershell prompt.
Write down the policy that you have in place. This should be your default Powershell execution policy.
Notice that once we finish running the Powershell script we should return back the execution policy to default.

To run Powershell scripts at the Powershell prompt, type Set-ExecutionPolicy Unrestricted
When prompted with a question "if you are sure that you want to change the Execution Policy" hit the enter button again. 

Now that you are able to run Powershell scripts navigate to where you have placed the Powershell script.

Before we run our powershell script we also need to install a third party library that we need.
To do so simply click on PCSX-1.2.msi installer. Follow the prompts and click on Next. 
This installer will install the third party libraries that are in use while running this script. 
The third party libraries are part of the PowerShell Community Extension Sources. 

Now lets go to the Powershell script location.

$cd  C:\Diagnostics

Invoke the powershell script with the following command

$powershell  .\Diagnostics.ps1

You should be able to run the script.

Once the script finishes run the command Set-ExecutionPolicy again with the default policy to set it back to original Powershell execution policy.

Understanding The Results
--------------------------

The script will produce the following .txt files in a Logs folder. It will also zip all these files into a logs.zip file.

Diagnostics.log -->This is the log file of the script itself
SystemInfo.-->Information about the Operating System
HardwareInfo.log -->Information about the system hardware.
NetworkInfo.log -->Information about the network connection.
Patches.txt --> All the system patches that have been applied
Security_Events -->Windows Security Event logs.
Application_Events.log --> Windows Application event logs
System_Events.txt --> Windows System Event logs.

When the script finishes executing, a zipped file Log.zip will be created that will contain all the log files.

