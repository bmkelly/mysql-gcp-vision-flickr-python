###


# Import images

import load_everything
######## Begin Settings ########
#### Flickr settings #### 
username='friskodude'
api_secret = '?'
api_key = '?'

number_photos_for_vision_data = 2

#### MySQL database settings ####
sql_host='localhost' 
sql_user='bmkelly'
sql_passwd=''
sql_db='project_muy'

######## End Settings ########

load_everything.import_flickr_images(username,api_key,api_secret)
load_everything.get_response_from_GCP_Vision(username,num_photos=number_photos_for_vision_data)
load_everything.parse_JSON_responses_into_database(username,sql_host,sql_user,sql_passwd,sql_db)


### Display ###
import database_utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# Get image_location
cur = database_utils.get_cursor()
db_index,path_to_img,labels,scores = database_utils.get_image_info(cur)

# String to place on top of image
output_text = ''
for i in xrange(len(labels)):
  output_text = output_text + ', ' + labels[i] + ' ' + str(scores[i])

output_text = output_text[2:-1]

# Open img
img = Image.open(path_to_img)
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
#font = ImageFont.truetype("sans-serif.ttf", 16)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((0, 0),output_text,(255,255,255))
img.save('sample-out.jpg')




