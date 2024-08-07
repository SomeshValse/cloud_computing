from urllib.parse import urlparse
import boto3
import json 
from pprint import pprint
import requests
import os
import logging

# resource will be used instead of client
s_3 = boto3.client(
    's3',
    aws_access_key_id= "ASIAZI2LBXUE6AQ6DSHY",
    aws_secret_access_key= "cw80KgLloKMLji8O+5X6+orR64kEbgls8t+1rlrN",
    aws_session_token= "IQoJb3JpZ2luX2VjEMf//////////wEaCXVzLXdlc3QtMiJHMEUCIQDbKcpM4pu0QWCXQc6CiD0nm2fy7C3+yw4aKrLX5WlXnQIgCK5a7r4gY8SvigZXJY95w9m1S5ue+mOBOa87Zs2v87wqvwIIoP//////////ARAAGgw2Mzc0MjMxNzI4NzMiDIJviBMuwZMolJjtMCqTAod2SUk7k3OTtXIBhuqLhRmsfKV2xxHNfFV8wjZLjaLZaWYqvgURcTXyUePwn8E2IS1rpkpc/e5VkqT+OTB46+Ha/YxemSRjC5MCqw+TfFs8jsy/8cNadcTOD8c+ft5qGaUmQo9ikcLkR48AmLtcW9Vkxwjlmm2Wpq6U+1ygC1t9q0uwZqAnaxi9pviUl+2e4Wn70IKIArLu5AWJwQ3AYZLSXFO0CV+xAcnPqZ0ypPMx8YgQAbipUBVzzIfz8qaQ6pPgFyCvBDDn0fqSf1XeLZR/DBg1IEW6qZgMgiN45DoHF9zwXJ5mxLNFoHgE+LSyEPTG350hWFVrYD49BCSHTzIBPxpXEPJ1LNInFfBIaayBhq6rMKDCgrUGOp0BFR+JYmm0cvlUApU/X9ii4GRhiJMqhswJj8oDyftX9K+x7Vy6bhL2TMizQ/HFfJCwL0cLfILv40fuRXCrHdRbBkWnsJA0b1752YEvPff5PhDzJuHlC4HMZbIPTO2oqPZLfYNuL+UWLFsUdS2f5NlM9+6kojLQkSSYFHuy6b5Ba2JKLqeqoHMlLvDvofGXBBaYuUCgPNRlCITEnVYAmg==",
    region_name= "us-east-1"
)

# Enable logging for boto3
logging.basicConfig(level=logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)

#creating the s3 bucket

bucket_name = input("Input Bucket Name: ") # enter name of bucket to create

def bucketname(resource, bucket_name):
    
    x = resource.create_bucket(Bucket=bucket_name)
    
    return x 

if __name__ == "__main__":
    # call the function 
    bucket = bucketname(s_3, bucket_name)
    # wait till bucket is created 
    waiter = s_3.get_waiter('bucket_exists')
    waiter.wait(Bucket=bucket_name)
    
    logger.info("Bucket Created: %s", bucket_name)


# reading json file 

with open('D:/Cloud_Computing/JSON-DynomoDB/a1.json', 'r') as file:
    x = json.load(file)
pprint(x)

# Using while loop iterating through the songs list and capturing img_url 

img_list = []

index = 0
while index < len(x["songs"]):
    song = x["songs"][index]
    img_url = song["img_url"]

    #create dictonary 
    img_dict = {
        "img_url":img_url
    }

    # append this dictonary to the list
    img_list.append(img_dict)

    #increment the counter
    index += 1

#print the result
pprint(img_list)

#count of list
print(len(img_list)) 

# downloading the images from the url 

# #create a directory to store the images for the check 
# os.makedirs("downloaded_images", exist_ok=True)

#Download the images from the urls
for idx, img_list in enumerate(img_list, start=1):
    
    y = img_list['img_url']
    
    #pprint(y) # check for url present 

    filename = f"downloaded_images/image_{idx}.jpg"
    response = requests.get(y)

    pprint(response) # response check (200 ok)

    if response.status_code == 200:
        # extract the artist name from the url 
        parsed_url = urlparse(y)
        artist_name = os.path.splitext(os.path.basename(parsed_url.path))[0]

        #generate key with artist name
        key = f"{artist_name}.jpg"

        #upload image to S3 bucket
        s_3.put_object(Bucket=bucket_name, Key=key, Body=response.content)
        
        print(f"Upload {artist_name}.jpg to S3 bucket")
    else:
        print(f"Failed to download {y}")

print("All images uploaded successfully to s3 bucket")






