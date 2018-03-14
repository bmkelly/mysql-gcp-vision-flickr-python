# mysql-gcp-vision-flickr-python

An example image with it's labels superimposed can be seen here:
![Example image](sample-out.jpg?raw=true "Example image with label superimposed")

This project uses google's vision api to characterize flickr images.  
Images and labels are stored in a mysql database.

To run this, you will need python2.7 with the following packages: Pillow, MySQLdb, flickr_api (https://github.com/alexis-mignon/python-flickr-api)

If you run this on a fresh Debian GNU/Linux 9 (stretch) install, here are the necessary installation commands.

**GIT install and download repo**
* sudo apt-get update
* sudo apt-get upgrade -y
* sudo apt-get install git -y
* git clone https://github.com/bmkelly/mysql-gcp-vision-flickr-python.git

**Python packages needed to install**
* sudo apt-get install python-pip -y
* pip install flickr_api -y
* pip install mysqlclient -y
* sudo apt-get install python-mysqldb -y
* pip install Pillow

**MySQL install and setup**
* sudo apt-get install mysql-server -y
* sudo mysql_secure_installation -y
* sudo mysql_install_db -y
* sudo mysql -u root -p
* CREATE USER bmkelly;
* GRANT ALL PRIVILEGES ON *.* TO 'bmkelly' IDENTIFIED BY '';
* exit
* mysql -u bmkelly
* run code in database_creation.sql

**Run the code**
Run main_args.py filling in the necessary arguments (-h command to get help info), or run main.py changing the variables manually.
If following this example exactly, the only necessary arguments are flickr_api_key and flickr_api_secret.

First, the the images will be downloaded:
![first_part](first_part.PNG?raw=true "Images being downloaded")

Then the labels from googles vision servers will be requested, saved, and stored:
![second_part](second_part.PNG?raw=true "Labels stored")

The database created has the following schema: 
![Database Schema](database_schema.jpg?raw=true "Database Schema")




