import MySQLdb
import json
import sys
import os
from os import listdir
from os.path import isfile, join
import codecs




# Insert a row into the photo table
def insert_photo(path,name,Photographer,cur):
  # If already exists, then skip
  if cur.execute("SELECT * FROM Photo WHERE Name LIKE '" + name + "';") > 0: 
    cur.fetchall()
    print('Photo ' + path + ' already in database')
    return
  
  num_similar = cur.execute("SELECT * FROM Photographer WHERE Username LIKE '"+ Photographer+"'")
  resp = cur.fetchall()
  print('Adding photo: ' + path + ' to database')
  if num_similar >0:
    photographer_ID = resp[0][0]
    cur.execute("INSERT INTO Photo(Path,Name,PhotographerID) VALUES('" \
                +path +"','" + name + "'," + str(photographer_ID) + ")")
    cur.fetchall()
  else:
    cur.execute("INSERT INTO Photo(Path,Name) VALUES('" \
                +path +"','" + name + "')")
    cur.fetchall()
    
# Insert a new label into the label table, related to the photo in photo table
def insert_label(score,topicality,mid,description,image_name,cur):
  # If already exists, then skip
  if cur.execute("SELECT * FROM Label WHERE Score - " + str(score) + " <.0001 AND " \
                "Topicality - " + str(topicality) + " <.0001 AND Mid LIKE '" + mid \
                 + "' AND Description LIKE '" + description + "';") > 0: 
    cur.fetchall()
    print('label for image_name:' + image_name+ ' is already in database, skipping.')
    return
  
  num_similar = cur.execute("SELECT * FROM Photo WHERE Name LIKE '"+ image_name+"'")
  resp = cur.fetchall()
  if num_similar ==1:
    image_ID = resp[0][0]
    cur.execute("INSERT INTO Label(Score,Topicality,Description,ImageID,Mid) VALUES(" \
                  +str(score) +"," + str(topicality) + ",'" + description + "'," + \
                  str(image_ID) + ",'"+ mid + "')")
    cur.fetchall()
  else:
    print("No photo to link to, which is weird")
    cur.execute("INSERT INTO Label(Score,Topicality,Description,Mid) VALUES(" \
                  +str(score) +"," + str(topicality) + ",'" + description + \
                  "','"+ mid + "')")
    cur.fetchall()
# Parse the label_dict to clean up code a bit
def parse_label_dict(label_annotation):
  score = label_annotation['score']
  topicality = label_annotation['topicality']
  mid = label_annotation['mid']
  description = label_annotation['description']
  return score,topicality,mid,description

def get_cursor(sql_host='localhost',sql_user='bmkelly',sql_passwd='',sql_db='project_muy'):
  db = MySQLdb.connect(host=sql_host,  # your host 
                     user=sql_user,       # username
                     passwd=sql_passwd,     # password
                     db=sql_db)   # name of the database
 
  # Create a Cursor object to execute queries.
  cur = db.cursor()
  return cur

def get_image_info(cur,index=0):
  cur.execute("SELECT * FROM Photo;")
  resp = cur.fetchall()
  db_index = resp[index][0]
  path = resp[index][1]
  cur.execute("SELECT * FROM Label WHERE ImageID = " + str(db_index) + ";")
  resp = cur.fetchall()
  labels = []
  scores = []
  for r in resp:
    labels.append(r[4])
    scores.append(r[1])
  
  return db_index,path,labels,scores


# EoF #
