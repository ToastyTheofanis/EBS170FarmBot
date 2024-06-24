
import requests
import urllib.request 
import os
#Grabs API Token using log in information 
def get_token():
    global token
    token = None
    if not token:

        # Get your FarmBot Web App token.
        headers = {'content-type': 'application/json'}
        
        #Log in information
        user = {'user': {'email': "jiroach@ucdavis.edu", 'password': "ebs170FB"}}
        response = requests.post('https://my.farmbot.io/api/tokens',
                                 headers=headers, json=user)
        token = response.json()['token']['encoded']

    return token

#Grabs authorization headers with the API token
def get_headers():

    headers = {'Authorization': 'Bearer ' + get_token(),
               'content-type': "application/json"}
    return headers

def download_images():

    #Gets meta data about images from Message Broker
    response = requests.get('https://my.farmbot.io/api/images', headers=get_headers())
    images = response.json()
    
    #print(json.dumps(latestImage, indent=2))
    
    #Change path depending on user
    dest_direc = "C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/Images/"

    #Saves the url's image to a folder
    for i in images:

        filename = dest_direc + os.path.basename(i["attachment_url"]) + ".jpg"
        #print(filename)

        urllib.request.urlretrieve(i["attachment_url"], filename)


download_images()

