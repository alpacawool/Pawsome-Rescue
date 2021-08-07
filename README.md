# Pawsome Rescue
##### Created by Wes MacDonald and Patricia Booth 

Pawsome Rescue is an web application that aims to help pets find happy homes. Users are can view available animals, add new animals, and apply for animals for a variety of shelters. This project was built with HTML, CSS,  and JavaScript using Flask as the server backend and Jinja for templating. This was created for CS 340 - Introductions to Databases. 

![](https://media1.giphy.com/media/ApK7RMUfQ60bfMM3YY/giphy.gif)

[Demo](https://paw-some.herokuapp.com/ "Demo")

## Requirements

- Python 3.9+
- MySQL database
- Cloudinary Account

## Installation

- Create a file named .env in the root directory and add the following environmental variables.
```
DB_USER = db_username
DB_PW = db_password
DB_HOST = db_host
DB_NAME = db_name
DB_PORT = db_port
CLOUD_NAME = cloudinary_cloud_name
API_KEY= cloudinary_api_key
API_SECRET = cloudinary_api_secret
```
-  Run the following commands in the project directory
```bash
pip install -r requirements.txt
python -m flask run 
```
