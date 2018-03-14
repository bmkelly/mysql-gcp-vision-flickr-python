import argparse
parser = argparse.ArgumentParser(description='Flickr Image Downloader and Characterization via GCP Vision API')

parser.add_argument('--flickr_username', default='friskodude', type=str,
                    help='Username of flickr user from which to download images')
parser.add_argument('--flickr_api_secret', default='?', type=str,
                    help='API Secret for flickr API, see README for instructions on getting API secret')
parser.add_argument('--flickr_api_key', default='?', type=str,
                    help='API key for flickr API, see README for instructions on getting API key')
parser.add_argument('--sql_host', default='localhost', type=str,
                    help='MySQL server, default is locally hosted')
parser.add_argument('--sql_user', default='bmkelly', type=str,
                    help='MySQL server username')
parser.add_argument('--sql_passwd', default='', type=str,
                    help='MySQL password')
parser.add_argument('--sql_db', default='project_muy', type=str,
                    help='Database within MySQL server.  Instructions on setting up db is found in README')
parser.add_argument('--num_imgs', default=2, type=int,
                    help='Number of images to acquire characterization from gcp vision server.  If not run on gcp server, may experience errors using this.')
parser.add_argument('--save_test_img', default=True, type=bool,
                    help='If true, this will save a sample image to sample-out.jpg.')
args = parser.parse_args()


import load_everything
load_everything.import_flickr_images(args.username,args.api_key,args.api_secret)
load_everything.get_response_from_GCP_Vision(args.username,args.num_imgs)
load_everything.parse_JSON_responses_into_database(args.username,args.sql_host,args.sql_user,args.sql_passwd,args.sql_db)


if args.save_test_img:
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
  draw.text((0, 0),output_text,(255, 255, 255))
  img.save('sample-out.jpg')







 # EoF #
