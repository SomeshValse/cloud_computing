import logging
import boto3 
import json
from pprint import pprint

# Enable logging for boto3
logging.basicConfig(level=logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)


#DynamoDb configuration
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id= "ASIAZI2LBXUE6AQ6DSHY",
    aws_secret_access_key= "cw80KgLloKMLji8O+5X6+orR64kEbgls8t+1rlrN",
    aws_session_token= "IQoJb3JpZ2luX2VjEMf//////////wEaCXVzLXdlc3QtMiJHMEUCIQDbKcpM4pu0QWCXQc6CiD0nm2fy7C3+yw4aKrLX5WlXnQIgCK5a7r4gY8SvigZXJY95w9m1S5ue+mOBOa87Zs2v87wqvwIIoP//////////ARAAGgw2Mzc0MjMxNzI4NzMiDIJviBMuwZMolJjtMCqTAod2SUk7k3OTtXIBhuqLhRmsfKV2xxHNfFV8wjZLjaLZaWYqvgURcTXyUePwn8E2IS1rpkpc/e5VkqT+OTB46+Ha/YxemSRjC5MCqw+TfFs8jsy/8cNadcTOD8c+ft5qGaUmQo9ikcLkR48AmLtcW9Vkxwjlmm2Wpq6U+1ygC1t9q0uwZqAnaxi9pviUl+2e4Wn70IKIArLu5AWJwQ3AYZLSXFO0CV+xAcnPqZ0ypPMx8YgQAbipUBVzzIfz8qaQ6pPgFyCvBDDn0fqSf1XeLZR/DBg1IEW6qZgMgiN45DoHF9zwXJ5mxLNFoHgE+LSyEPTG350hWFVrYD49BCSHTzIBPxpXEPJ1LNInFfBIaayBhq6rMKDCgrUGOp0BFR+JYmm0cvlUApU/X9ii4GRhiJMqhswJj8oDyftX9K+x7Vy6bhL2TMizQ/HFfJCwL0cLfILv40fuRXCrHdRbBkWnsJA0b1752YEvPff5PhDzJuHlC4HMZbIPTO2oqPZLfYNuL+UWLFsUdS2f5NlM9+6kojLQkSSYFHuy6b5Ba2JKLqeqoHMlLvDvofGXBBaYuUCgPNRlCITEnVYAmg==",
    region_name= "us-east-1"
)

# # Dynamodb local config
# dynamodb_local = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name= "us-east-1"
# )

table_name = input("Input Table Name: ") # enter name of table to create

def create_table(resource, table_name):    # function defined for create_table
    x = resource.create_table(           
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'  # Partition Key
            },
            {
                'AttributeName': 'year',
                'KeyType': 'RANGE'  # Sort Key
            }
        ],
        AttributeDefinitions=[  # Define attribute types
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'year',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return x

if __name__ == "__main__":
    #we call the function
    table = create_table(dynamodb, table_name)
    # Wait for the table to be created
    waiter = dynamodb.meta.client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    
    logger.info("Table Created: %s", table.table_name)

#################################################################################################

# pushing data into dynamodb 

# with open('D:/Cloud_Computing/S3951107_APP_DEVELOPMENT/a1.json', 'r') as file:
#     x = json.load(file)

#     #print(x)

# # Initialize an empty list to store dictionaries
# songs_list = []

# # Use a while loop to iterate through the songs and capture title, artist, year, web_url and img_url from the json file
# index = 0
# while index < len(x["songs"]):
#     song = x["songs"][index]
#     title = song["title"]
#     artist = song["artist"]
#     year = song["year"]
#     web_url = song["web_url"]
#     img_url = song["img_url"]

#     # Create a dictionary for the current song
#     song_dict = {
#         "title": title,
#         "artist": artist,
#         "year": year,
#         "web_url": web_url,
#         "img_url": img_url
#     }

#     # Append the dictionary to the list
#     songs_list.append(song_dict)

#     # Increment the index
#     index += 1

# # Print the resulting list of dictionaries
# pprint(songs_list)

# table = dynamodb.Table(table_name)

# # iterating over list of songs and using put_item() function appending the dynamodb table with new entry
# for i in range(0, len(songs_list)):
#     table.put_item(Item = songs_list[i])


