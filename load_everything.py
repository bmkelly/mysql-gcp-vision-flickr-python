### Import flickr images ###

# Username is the username of the flickr user.
# API key and secret can be aquired by signing up on yahoo
def import_flickr_images(username='friskodude',api_key='??',api_secret='??'):
  import flickr_api
  import os
  
  flickr_api.set_keys(api_key,api_secret)

  user = flickr_api.Person.findByUserName(username)
  photos = user.getPhotos()

  photo_dir = username+'_photos/'

  if not os.path.exists(photo_dir):
    print("Creating directory " + photo_dir)
    os.mkdir(photo_dir)


  for photo in photos:
    print("Saving photo " + photo.title)
    photo.save(photo_dir+photo.title+".jpg")

  
### Use python to interface with GCP vision api ###

def get_response_from_GCP_Vision(username='friskodude',num_photos=2):
  import base64
  import json
  import sys
  import os
  from os import listdir
  from os.path import isfile, join

  DETECTION_TYPES = [
      'TYPE_UNSPECIFIED',
      'FACE_DETECTION',
      'LANDMARK_DETECTION',
      'LOGO_DETECTION',
      'LABEL_DETECTION',
      'TEXT_DETECTION',
      'SAFE_SEARCH_DETECTION',
  ]

  # load filenanes
  photo_dir = username+'_photos/'
  photo_filenames = [f for f in listdir(photo_dir) if isfile(join(photo_dir, f))]

  photo_response_dir = username + '_photo_responses/'
  if not os.path.exists(photo_response_dir):
    print("Creating directory " + photo_response_dir)
    os.mkdir(photo_response_dir)

  # for each photo, create request file, send request, save response in photo_response_dir
  print("For each of "+ str(len(photo_filenames)) + " photos creating request file, sending request, and saving response to "+ photo_response_dir + "name_response.json")
  counter = 0
  for pf in photo_filenames[0:num_photos]:
    pf = pf[0:-4]
    print("Working on photo " + str(counter) + " file: "+ pf)
    counter+=1
    request_filename = photo_response_dir+ pf+ '_request.json'
    response_filename = photo_response_dir+ pf + '_response.json'

    # generate request filename
    request_list = []
    with open(photo_dir+pf +'.jpg','rb') as image_file:
      content_json_obj = {
        'content': base64.b64encode(image_file.read()).decode('UTF-8')
        }

      feature_json_obj = []
      feature_json_obj.append({
        'type': 'LABEL_DETECTION',
        'maxResults': 3,
      })
  #     feature_json_obj.append({
  #       'type': 'FACE_DETECTION',
  #       'maxResults': 3,
  #     })
      request_list.append({
        'features': feature_json_obj,
        'image': content_json_obj,

      })

      with open(request_filename,'w') as output_file:
        json.dump({'requests': request_list}, output_file)

      # send the request to Cloud Vision and display the response
      import requests
      data = open(request_filename, 'rb').read()
      response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDpF0cROMjZ6DvE8-XbFif4kO-sZwqr2NM',
          data=data,
          headers={'Content-Type': 'application/json'})

      # save reponse file
      with open(response_filename,'w') as output_file:
        output_file.write(response.text)



      
### Load JSON responses ###
def parse_JSON_responses_into_database(username='friskodude',sql_host='localhost',sql_user='bmkelly',sql_passwd='',sql_db='project_muy'):
  import json
  import sys
  import os
  from os import listdir
  from os.path import isfile, join
  import codecs
  from database_utils import insert_photo,insert_label,parse_label_dict
  import MySQLdb
  from contextlib import closing
  reader = codecs.getreader("utf-8")

  db = MySQLdb.connect(host=sql_host,  # your host 
                     user=sql_user,       # username
                     passwd=sql_passwd,     # password
                     db=sql_db)   # name of the database
  # Create a Cursor object to execute queries.
  with closing(db.cursor()) as cur:
    # Initially create Photographer user
    num_similar = cur.execute("SELECT * FROM Photographer WHERE Username LIKE '"+ username+"'")
    cur.fetchall()
    # but only if not already in database
    if num_similar>1:
      print('num_similar:' + str(num_similar) + ' which it shouldnt be.  It should only be 1 or 0.')
    if num_similar<1:
      cur.execute("INSERT INTO Photographer(Username) VALUES ('" + username + "')")
      cur.fetchall()

    # acquire all response filenames
    photo_response_dir = username + '_photo_responses/'
    photo_response_filenames = [f for f in listdir(photo_response_dir) if (isfile(join(photo_response_dir, f)) and ("_response" in f))]
    photo_dir = username + '_photos/'
    # for each response filenames, load file, parse json, print out, insert into database
    for r in photo_response_filenames:
      with open(photo_response_dir + r,'rb') as rf:
        parsed_rf = json.load(reader(rf))

        current_filename = r[0:-1*len('_response.json')]

        print(current_filename)

        # Insert into database
        insert_photo(photo_dir+current_filename + '.jpg',current_filename,username,cur)
        for label_annotation in parsed_rf['responses'][0]['labelAnnotations']:
          score, topicality, mid, description = parse_label_dict(label_annotation)
          insert_label(score,topicality,mid,description,current_filename,cur)
          print(label_annotation)

    db.commit()
    db.close()

    

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

# EoF #
