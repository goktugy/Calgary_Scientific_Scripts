echo "Please provide the database name in PostgreSQL to connect"
echo "This is the same database name that you used in the data server"
read database_name
echo "You entered: $database_name"
sed -i  "s/pacsdb/$database_name/g"  /root/dcm4chee/dcm4chee-2.18.0-psql/server/default/deploy/pacs-postgres-ds.xml
sed -i  "s/localhost/data-server/g"  /root/dcm4chee/dcm4chee-2.18.0-psql/server/default/deploy/pacs-postgres-ds.xml

if [ $? -eq 0 ]; then 
   echo "Successfully changed the database name to $database_name"
else   
   echo "Could not change the database name to $database_name" 
   exit 1
fi

echo "Please provide the user name in PostgreSQL to connect"
echo "This is the same user user name that you created in the data server"
read user_name
echo "You entered: $user_name"
perl -i -pe "s/postgres/$user_name/ if $.==20"  /root/dcm4chee/dcm4chee-2.18.0-psql/server/default/deploy/pacs-postgres-ds.xml

if [ $? -eq 0 ]; then 
   echo "Successfully changed the user name to $user_name"
else   
   echo "Could not change the user name to $user_name" 
   exit 1
fi

echo "Creating required tables into the PACS database"
psql -h data-server -d $database_name -U $user_name -f ~/dcm4chee/dcm4chee-2.18.0-psql/sql/create.psql

if [ $? -eq 0 ]; then 
   echo "Successfully created the required tables"
else   
   echo "Could not create the required tables" 
   exit 1
fi

echo "Please provide the name of the folder you would like to mount to PACS Storage"
echo"This is the same folder as the folder you created for PACS-Storage in the data server"
read PACS_Storage
echo "Mounting the PACS Storage folder"
mount 10.229.0.250:/media/PACS-Storage/$PACS_Storage /mnt/pacs-storage/

if [ $? -eq 0 ]; then 
   echo "Successfully mounted PACS Storage folder"
else   
   echo "Could not mount the PACS Storage folder" 
   exit 1
fi

echo "Setting entries in the /etc/fstab file"
echo "10.229.0.250:/media/PACS-Storage/$PACS_Storage  /mnt/pacs-storage  nfs defaults 0 0" >> /etc/fstab 
if [ $? -eq 0 ] ; then 
   echo "Successfully editted /etc/fstab file"
else   
   echo "Could not edit /etc/fstab file" 
   exit 1
fi
