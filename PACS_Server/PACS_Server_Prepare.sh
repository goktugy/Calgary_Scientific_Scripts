echo "Please provide the correct MAC address for this PACS server"
read MAC_Address
echo "You provided MAC Address : $MAC_Address"
echo "Deleting the wrong MAC address entry from /etc/udev/rules.d/70-persistent-net.rules"
sed -i "/eth0/d" /etc/udev/rules.d/70-persistent-net.rules

if [ $? -eq 0 ]; then 
   echo "Successfully deleted the wrong MAC address"
else   
   echo "Could not delete the wrong MAC address" 
   exit 1
fi

echo "Deleting the second wrong MAC address entry from /etc/udev/rules.d/70-persistent-net.rules"
sed -i "/eth1/d" /etc/udev/rules.d/70-persistent-net.rules

if [ $? -eq 0 ]; then 
   echo "Successfully deleted the second wrong MAC address"
else   
   echo "Could not delete the wrong MAC address" 
   exit 1
fi

echo "Replacing eth2 to eth0 in the file /etc/udev/rules.d/70-persistent-net.rules"
sed -i "s/eth2/eth0/g" /etc/udev/rules.d/70-persistent-net.rules

if [ $? -eq 0 ]; then 
   echo "Successfully replaced eth2 to eth0"
else   
   echo "Could not replace eth2 to eth0" 
   exit 1
fi


echo "Replacing the HWADDR field with the right MAC address at /etc/sysconfig/network-scripts/ifcfg-eth0"
sed -i  "s/^HWADDR=.*/HWADDR=$MAC_Address/g" /etc/sysconfig/network-scripts/ifcfg-eth0

if [ $? -eq 0 ]; then 
   echo "Successfully replaced HWADDR field"
else   
   echo "Could not replace HWADDR field" 
   exit 1
fi
