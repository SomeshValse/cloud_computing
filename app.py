from urllib import request
from flask import Flask, redirect, url_for, session, render_template, request, jsonify
import boto3
import requests
from boto3.dynamodb.conditions import Key, Attr

### WSGI application

app = Flask(__name__) #flask object to start our flask application 

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

app.secret_key = b'sam@9820'

##########################################################################
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/check', methods = ['GET', 'POST']) 
def check():
    if request.method == 'POST':                # if the method is POST, we are accepting input email and password from the user 
        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table('login-table')  # we are connecting to the login-table by using dynamodb resources
        response = table.query(
            KeyConditionExpression=Key('email').eq(email) # then, we are checking whether entered email is present in login-table 
        )
        items = response['Items']                         # if yes, then we are storing the whole row assiocated with that email in item variable, as we have set email our partition key
        if items:
            user_name = items[0]['user_name']
            if password == items[0]['password']:          # checking whether entered password matches password stored in dynamodb login-table
                session['username'] = user_name
                return redirect(url_for('main', username=user_name)) #redirecting to main page

    return render_template('login.html', error = 'email or password is invalid') # if both email and password are invalid, we are rendering template with message

###################################################################################

@app.route('/register') 
def register():
    return render_template('register.html') 

@app.route('/registercheck', methods = ['GET','POST'])
def registercheck():
    if request.method == 'POST':                # if method is POST, we are accepting email, user_name and password from the user
        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        # create a dictonary for sending it to API REST Gateway, in which we have created '/register' resource and method 'POST' which will trigger lambda function
        data = {
            "email": email,
            "user_name": user_name,
            "password": password
        }

        # URL for API REST lambda function 
        lambda_fun_URL = "https://juthgi8la4.execute-api.us-east-1.amazonaws.com/prod_2/register"

        # making a request to lambda function API endpoint
        response = requests.post(lambda_fun_URL, json = data)

        if response.status_code == 200:        # Once, entry gets added into login-table, it will redirect to login page 
            return redirect(url_for('login'))
        else:
            print("The email entered already exists")  # else, it will render template by printing the message 
            return render_template('register.html', message='The email entered already exists')

   # If the request method is not 'POST', return the register page
    return render_template('register.html')
        
##################################################################################################

@app.route('/main/<username>') 
def main(username):
    username = session.get('username')  # we are getting the user_name from the session 

    if not username:
        return redirect(url_for('login'))

    table = dynamodb.Table('music_sub')  # we have created subscribed music table, where we are going to store all subscribed music 

    response_sub = table.scan()         # we are scanning the content of that table 

    items_sub = response_sub['Items']  # we are storing all info regarding Title, year, artist and Image in item_sub variable 

    items_query = session.get('items_query', []) # we are storing query info so that we can diplay in main page in item_query variable 
    message = session.get('message')             # storing the message from query area 

    return render_template('main.html', items=items_sub, items_query = items_query, message = message, user_name=username) # rendering the main page with items from table, query info and message with user_name

@app.route('/remove/<title>/<artist>/<year>/<path:img_url>') # we are accepting the 'GET' request from AJAX 
def entry_remove(title, artist, year, img_url):
    
    #storing the data in dict format and then passing it to API gateway REST in which we have created resource '/delete' with method delete which will trigger lambda function
    data = {
        'title': title,
        'year': year
    }

    # URL for lambda function 
    lambda_fun_URL = "https://juthgi8la4.execute-api.us-east-1.amazonaws.com/prod_2/delete"

    # making a request to lambda function API endpoint
    response = requests.delete(lambda_fun_URL, json = data)

    if response.status_code == 200:                            # when our response is 200 (OK), we will be redirected to main page 
        return redirect(url_for('main', username='username'))
    else:
        return jsonify({'error': 'Failed to delete item'}) # else, it will give message failed to delete item 

#########################################################################################

# @app.route('/query') 
# def query():
#     return render_template('query.html')

@app.route('/querycheck', methods=['POST'])     # here, we are accepting input from the user and method we are using POST 
def query_check():
    title = request.form.get('title')
    year = request.form.get('year')
    artist = request.form.get('artist')

    table = dynamodb.Table('music')            # access the table music from the dynamodb resources 

    
    params = {}                                     # define dictonary to collect the data provided by input 
    exp_attr_name = {}                              # we are defining exp_attr_name to handle the error occured (reserved word error)

    if title:                                       # if user entered title 
        params['title'] = title
        exp_attr_name['#title'] = 'title'           # handling reserve word for title
    if year:                                        # if user entered year 
        params['year'] = year
        exp_attr_name['#year'] = 'year'             # handling reserve word for year
    if artist:                                      # if user entered artist 
        params['artist'] = artist
        exp_attr_name['#artist'] = 'artist'         # handling reserve word for artist
    
    
    flt_exp_par = [f"#{i} = :{i}" for i in params]  # we are iterating over the stored parameter and producing list of strings where '#{i}' acts like placeholder for attribute name, 
    filter_expression = ' and '.join(flt_exp_par)   # ':{i}' acts like attribute value. for example, [#title = :title, #year = :year, #artist = :artist]
                                                    # joining these strings with AND operator 
    
    response = table.scan(
        FilterExpression=filter_expression,
        ExpressionAttributeNames=exp_attr_name,
        ExpressionAttributeValues={f":{x}": y for x, y in params.items()}
    )

    items_query = response.get('Items', [])

    message = "No result is retrieved. Please query again." if not items_query else None   # if nothing is present in item_query variable it will post message No result retrived else None

    session['items_query'] = items_query
    session['message'] = message

    return redirect(url_for('main', username=session.get('username'))) # it wil redirect to main page with user_name 

''' Code adapted from StackOverFlow and AWS boto3 Example: 
https://stackoverflow.com/questions/36698945/scan-function-in-dynamodb-with-reserved-keyword-as-filterexpression-nodejs , 
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/scan.html'''

from urllib.parse import unquote

@app.route('/update/<path:title>/<path:artist>/<path:year>/<path:img_url>')  # we are accepting the 'GET' request from AJAX for updating song info
def entry_update(title, year, artist, img_url):
    
    title = unquote(title)           # we are using unquote functionality to handle special character which we get from AJAX request 
    artist = unquote(artist)
    year = unquote(year)
    img_url = unquote(img_url)

    # storing the data in dict format and passing to REST API which will trigger lambda function 
    data = {
        'title':title,
        'artist':artist,
        'year':year,
        'img_url':img_url
    }

    # API gateway URL for lambda function 
    lambda_fun_URL = "https://juthgi8la4.execute-api.us-east-1.amazonaws.com/prod_2/query"

    # making a request to lambda function API endpoint
    response = requests.post(lambda_fun_URL, json = data)

    if response.status_code == 200:
        message = "Item added Successfully"
    if response.status_code == 400:
        message = "Item already exist"
    
    session['message'] = message

    return redirect(url_for('main', username=session.get('username')))

@app.route('/logout')
def logout():
    session.clear() # we are clearing the session after user click on logout link 
    return render_template('login.html')


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__': 
    app.run(host='0.0.0.0',port=80)