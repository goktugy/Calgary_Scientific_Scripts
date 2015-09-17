echo "Restoring original state"
echo "Unmounting /mnt/pacs-storage folder"
umount /mnt/pacs-storage

echo "Restoring 70-persistent-net.rules configuration file"
\cp ./Backup/70-persistent-net.rules.backup /etc/udev/rules.d/70-persistent-net.rules 

echo "Restoring ifcfg-eth0 file"
\cp ./Backup/ifcfg-eth0.backup /etc/sysconfig/network-scripts/ifcfg-eth0

echo "Restoring fstab file"
\cp ./Backup/fstab.backup /etc/fstab

echo "Restoring pacs-postgres-ds.xml"
\cp ./Backup/pacs-postgres-ds.xml.backup  /root/dcm4chee/dcm4chee-2.18.0-psql/server/default/deploy/pacs-postgres-ds.xml
 
 