import json
import requests
import urllib.request 
import os
from ultralytics import YOLO
import math


#Grabs API Token using log in information 
def get_token():
    global token
    token = None
    if not token:

        # Get your FarmBot Web App token.
        headers = {'content-type': 'application/json'}
        
        #Log in information
        user = {'user': {'email': "email", 'password': "password"}}
        response = requests.post('https://my.farmbot.io/api/tokens',
                                 headers=headers, json=user)
        token = response.json()['token']['encoded']

    return token

#Grabs authorization headers with the API token
def get_headers():

    headers = {'Authorization': 'Bearer ' + get_token(),
               'content-type': "application/json"}
    return headers

#Downloads images and saves to path
def download_images():

    #Gets meta data about images from Message Broker
    response = requests.get('https://my.farmbot.io/api/images', headers=get_headers())
    images = response.json()
    latestImage = images[0]
    
    #print(json.dumps(latestImage, indent=2))
    
    #Change path depending on user
    dest_direc = "C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/Images/"

    #Saves the url's image to a folder

    filename = dest_direc + os.path.basename(latestImage["attachment_url"]) + ".jpg"
    #print(filename)

    urllib.request.urlretrieve(latestImage["attachment_url"], filename)
        
        
def process_images(last_image):
  best = "C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/best.pt"
  model = YOLO(best)
  results = model.predict(last_image, save=True, conf=0.8, show=True, save_txt=True)

def find_last_image(directory):
    # List all files in the directory
    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    #Sort files by modification time
    files.sort(key=os.path.getmtime)

    #Return the last image file
    if files: 
        return files[0]
    else:
        return "No images found in the directory."
    
def find_last_predict(directory):
    #List all subdirectories in the directory
    directories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    #Sort directories by modification time
    directories.sort(key=os.path.getmtime)

    #Return the first directory
    if directories:
        print(directories[-1])
        path = os.path.join(directories[-1],'labels')
        txt_files = [os.path.join(path, file) for file in os.listdir(path) if file.lower().endswith('.txt')]
        print(txt_files[0])
        return (txt_files[0])
    else:
        return "No directories found in the directory."

def extract_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 3:  # Ensure there are at least three elements in the line
                # Append the second and third elements as a tuple (convert them to floats)
                coordinates.append((float(parts[1]), float(parts[2])))
    return coordinates

def get_coordinates():
    download_images()
    last_image = find_last_image("C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/Images/")
    process_images(last_image)

    predict_file_path = 'C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/runs/detect/'
    txtfile_path = find_last_predict(predict_file_path)
    norm_pixel_coordinates = extract_coordinates(txtfile_path)
    print(norm_pixel_coordinates)

get_coordinates()






