import flickr_api
import os

flickr_api.set_keys(api_key = '928b7e000b8b02f4a32eef0588294e0e', api_secret = '460a42489be7ce4d')

username = 'friskodude'
user = flickr_api.Person.findByUserName(username)
photos = user.getPhotos()

photo_dir = username+'_photos/'

if not os.path.exists(photo_dir):
  print("Creating directory " + photo_dir)
  os.mkdir(photo_dir)
 

for photo in photos:
  print("Saving photo " + photo.title)
  photo.save(photo_dir+photo.title+".jpg")

