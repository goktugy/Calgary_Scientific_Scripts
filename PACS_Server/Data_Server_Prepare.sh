echo "Please enter the name of the user you would like to create in PostgreSQL:"
read user_name
echo "You entered: $user_name"
echo "Creating user $user_name in PostgreSQL"

createuser -U postgres -S -d -R $user_name
if [ $? -eq 0 ]; then 
   echo "Successfully created user $user_name"
else   
   echo "Could not create user $user_name" 
   exit 1
fi
   
echo "Please enter the name of the database you would like to create in PostgreSQL:"
read database_name
echo "You entered: $database_name"
echo "Creating database $database_name in PostgrSQL with owner $user_name"

createdb -U postgres -O $user_name $database_name
if [ $? -eq 0 ]; then 
   echo "Successfully created database $databse_name with owner $user_name"
else   
   echo "Could not create database $database_name with owner $user_name" 
   exit 1
fi

echo "Please provide the name of the folder you would like to create for PACS Storage"
read PACS_Storage
echo "Creating folder for the PACS-Storage"
mkdir /media/PACS-Storage/$PACS_Storage

if [ $? -eq 0 ]; then 
   echo "Successfully created folder $PACS_Storage"
else   
   echo "Could not create folder $PACS_Storage" 
   exit 1
fi

echo "This directory will be mounted later from the PACS server machine"

echo "Please provide the IP address of the PACS server"
read IP_Address
echo "You provided $IP_Address"

string_to_add="/media/PACS-Storage/$PACS_Storage   " 
string_to_add+=$IP_Address
string_to_add+="(rw,sync,no_root_squash,no_subtree_check)" 
echo $string_to_add >> /etc/exports

if [ $? -eq 0 ]; then 
   echo "Successfully added IP address $IP_Address to /etc/exports"
else   
   echo "Could not add IP address $IP_Address to /etc/exports" 
   exit 1
fi


echo "Starting file system export"
exportfs -ra

if [ $? -eq 0 ]; then 
   echo "Successfully started file system export"
else   
   echo "Could not start file system export" 
   exit 1
fi


 
