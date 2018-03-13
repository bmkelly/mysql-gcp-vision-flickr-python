
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
username = 'friskodude'
photo_dir = username+'_photos/'
photo_filenames = [f for f in listdir(photo_dir) if isfile(join(photo_dir, f))]

photo_response_dir = username + '_photo_responses/'
if not os.path.exists(photo_response_dir):
  print("Creating directory " + photo_response_dir)
  os.mkdir(photo_response_dir)

# for each photo, create request file, send request, save response in photo_response_dir
print("For each of "+ str(len(photo_filenames)) + " photos creating request file, sending request, and saving response to "+ photo_response_dir + "name_response.json")
counter = 0
for pf in photo_filenames[0:2]:
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
    feature_json_obj.append({
      'type': 'FACE_DETECTION',
      'maxResults': 3,
    })
    
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



