#This script was written to retrieve Diagnostics information
#about Windows Operating System and ResolutionMD.
#
#


#These are global variables 

#Lets get the current date
$Now= Get-Date -format "dd-MMM-yyyy HH:mm"

#Retrieve current execution path
$scriptDir = Split-Path $script:MyInvocation.MyCommand.Path

#Create a folder to place all the log files.
$logFolder= $scriptDir+"\Logs" 

$folderCreated= New-Item $logFolder -type directory -force

#Logfile is used to store the location of the log file.
$Logfile = $scriptDir+"\Logs\Diagnostics.log"

Function LogWrite
#This function was written to record to a log file
#It takes the string parameter to write.
#Writes the string that is provided to the log file.

{
   Param ([string]$logstring)
   
   Add-content $Logfile -value $logstring
}


Function Welcome()
{
# This function was written to present the user with a Welcome page
#
#

Write-Host "Welcome To Pureweb Windows Diagnostic Analysis" 
Write-Host "This Script will gather information about the Operating System & ResolutionMD"
}



Function getSystem()
{
#This function takes as a parameter the log file where to write the data it retrieves.
#The function retrieves the following information from the system
#The name of the Operating System
#The amount of free memory
#Total memory capacity


#The function writes the data it retrieves to the log file.

Param ([string]$systemInfo)

"Today Is "+ $Now | Out-File $systemInfo

$os=Get-WmiObject -Class win32_operatingsystem

"Platform Distribution is "+$os.Caption | Out-File $systemInfo -Append

if ([System.IntPtr]::Size -eq 4) 
    {  
       "Machine Architecture is 32 bits "| Out-File $systemInfo -Append   
    } 
else 
    {  
       "Machine Architecture is 64 bits "| Out-File $systemInfo -Append 
    } 

$mem = Get-WmiObject -Class Win32_ComputerSystem 
"Total Memory is {0} MB" -f $([math]::Round($mem.TotalPhysicalMemory/1mb)) | Out-File $systeminfo -Append

"Available memory is {0} MB" -f $([math]::Round($os.FreePhysicalMemory/1kb)) | Out-File $systeminfo -Append


LogWrite "Retrieving Installed Software Information"
"`r`nCurrently the following software is installed :" | Out-File $systemInfo  -append
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |  Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table –AutoSize | Out-File $systemInfo -append -width 1500

"`r`nAdditionally the following software is installed :" | Out-File $systemInfo -append
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table –AutoSize | Out-File $systemInfo -append -width 1500    


LogWrite "Retrieving List of Running Services"
"`r`nCurrently these processes are running :" | Out-File $systemInfo -append
gwmi win32_service | where {$_.State -eq "Running"} | Out-File $systemInfo -append -width 1500 


LogWrite "Retrieving PureWebService Information"
"Information about PureWeb service" | Out-File $systemInfo -append
tasklist /fi "services eq PureWebLauncher" | Out-File $systemInfo -append -width 1500

}

Function getHardware()
{

#This function takes as a parameter the log file where to write the data it retrieves.
#The function retrieves the following information from the system
#System Runtime
#CPU average load 
#Current system CPU usage percentage



Param ([string]$hardwareInfo)

$date = get-date

$os=Get-WmiObject -Class win32_operatingsystem

$uptime = $os.ConvertToDateTime($os.lastbootuptime)
"The System has been running for "+ ($date- $uptime) | Out-File $hardwareInfo 

$cpu = Get-WmiObject -Class win32_processor | Measure-Object -property LoadPercentage -Average  
"The system's CPU has had an average load of " + $cpu.average + " percent" | Out-File $hardwareInfo -Append

$cpu_now = Get-WmiObject -Class win32_processor 
"The system current CPU usage is {0} percent" -f $($cpu_now.LoadPercentage) | Out-File $hardwareInfo -Append

"Bios information is the following :" | Out-File $hardwareInfo -append
get-wmiobject -class win32_bios | Out-File $hardwareInfo -append -width 1500

"Available disk space is the following:" | Out-File $hardwareInfo -append
get-wmiObject win32_logicaldisk | Out-File $hardwareInfo -append

}

Function getNetwork()
{
#This function takes as a parameter the log file where to write the data it retrieves.

#The function retrieves the following information from the system

#Windows Domain FireWall Status
#Windows Standard FireWall Status
#Windows Public FireWall Status
#The system hosts file
#Current ports that are in use.
#The system's IP address




Param ([string]$netWorkInfo)


#Check if the system firewall is on
    $cname = $env:computername  # get local host name 
    $reg = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey("LocalMachine",$cname)
    $DomainfirewallEnabled = $reg.OpenSubKey("System\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile").GetValue("EnableFirewall")
    $StandardfirewallEnabled = $reg.OpenSubKey("System\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile").GetValue("EnableFirewall")
    $PublicfirewallEnabled = $reg.OpenSubKey("System\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile").GetValue("EnableFirewall")
    
    If ($DomainfirewallEnabled -eq 1) {
        $CheckStatus = "Enabled" 
        "Windows Domain FireWall Is Enabled" | Out-File $networkInfo
    } else {
        $CheckStatus = "Disabled"
        "Windows Domain FireWall Is Not Enabled" | Out-File  $networkInfo -Append 
    }  

     If ($StandardfirewallEnabled -eq 1) {
        $CheckStatus = "Enabled" 
        "Windows Standard FireWall Is Enabled" | Out-File $networkInfo -Append 
        
    } else {
        $CheckStatus = "Disabled"
        "Windows Standard FireWall Is Not Enabled" | Out-File  $networkInfo -Append 
    }  

    If ($PublicfirewallEnabled -eq 1) {
        $CheckStatus = "Enabled" 
        "Windows Public FireWall Is Enabled" | Out-File $networkInfo -Append 
        
    } else {
        $CheckStatus = "Disabled"
        "Windows Public FireWall Is Not Enabled" | Out-File  $networkInfo -Append 
    }   

"`r`nThe following ports are in use :" | Out-File $networkInfo -Append
netstat -ano | Out-File $networkInfo -Append

"`r`nThe following is included in the hosts file :" | Out-File $networkInfo -Append
Get-Content C:\Windows\System32\drivers\etc\hosts | Out-File $networkInfo -Append


$ip = Get-WmiObject -Class Win32_NetworkAdapterConfiguration -Filter 'IPEnabled = True' 
"`r`nThe system's IP address are " | Out-File $networkInfo -Append
$ip | Out-File $networkInfo -Append

}


Function getPatches($patchInfo)
{

#This function takes as a parameter the 
#log file where to provide results.

#It lists all the pathes that were applied 
#to the system and writes them to a log file.


"Currently installed patches are :" | Out-File $patchInfo 
get-hotfix | Out-File $patchInfo -Append
}

Function getEventLogs
{

#This function takes as a parameter the 
#three diferent log file where to provide results.

#It will retrieve and list all the
#System, Application and Security logs.


Param ([string]$eventSystemLog,
       [string]$eventApplicationLog,
       [string]$eventSecurityLog
       )
       
"The event log contains the following for system events" | Out-File $eventSystemLog  -width 1500
Get-Eventlog System -newest 100 | Out-File $eventSystemLog -append -width 1500

"The event log contains the following for application events" | Out-File $eventApplicationLog -width 1500 
Get-Eventlog Application -newest 100 | Out-File $eventApplicationLog -append -width 1500

"The event log contains the following for security events" | Out-File $eventSecurityLog -width 1500 
Get-Eventlog Security -newest 100 | Out-File $eventSecurityLog -append -width 1500

}



####################################################################################################
#Main
Welcome

#Delete Existing Log File If It Exists
If(test-Path $Logfile)
  {Remove-Item $Logfile}

LogWrite "Starting Diagnostics"

#Lets get the current time

LogWrite ("Current Day And Time Is "+ $Now)

LogWrite ("Current Working Directory is " + $scriptDir)

#Let set the text file where we will store the system information
$systemInfo= $logFolder+"\SystemInfo.txt"

LogWrite "Retrieving System Information" 
getSystem $systemInfo 


LogWrite "Retrieving Hardware Information"
$hardwareLog= $logFolder+"\HardwareInfo.txt"
getHardware $hardwareLog

LogWrite "Retrieving Network Information"
$networkLog= $logFolder+"\NetworkInfo.txt"
getNetwork $networkLog


$patchInfo= $logFolder+"\Patches.txt"

LogWrite "Retrieving Patch Information"
getPatches $patchInfo

$eventSystemLog= $logFolder+"\System_Events.txt"
$eventApplicationLog= $logFolder+"\Application_Events.txt"
$eventSecurityLog= $logFolder+"\Security_Events.txt"

LogWrite "Retrieving Event Log Information"
getEventLogs $eventSystemLog $eventApplicationLog $eventSecurityLog

#Create a zip file to place all the log files.

$zipInput=  $logFolder
$zipOutput= $scriptDir +"\Logs.zip"
$zipResult= Write-Zip -LiteralPath $zipInput  -OutputPath $zipOutput