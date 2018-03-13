# mysql-gcp-vision-flickr-python

Using googles vision api to characterize flickr images.  Images and labels are stored in a mysql.

To run this, you will need python2.7 with the following packages: Pillow, MySQLdb, flickr_api (https://github.com/alexis-mignon/python-flickr-api)

You will need to have MySQL and create the database running the database_creation.sql file.
The database created has the following schema: 
![Database Schema](Database Scheme.jpg?raw=true "Database Schema")

An example image with it's labels superimposed can be seen here:
![Example image](sample-out.jpg?raw=true "Example image with label superimposed")


