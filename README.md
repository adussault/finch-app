# Finch-API Demo App

This is a simple demo app that creates a new Connection to the Finch Sandbox API with a specified provider and set of products. Once the connection is set up, the app pulls data from Finch's sandbox API and displays it in clean, readable tables. 


## Requirements:

- Runs on [Python 3.12](https://www.python.org/downloads/)
- You'll also need to install [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/) to handle session data.


## Python Dependencies

Python Libraries are listed in `requirements.txt`. You can install them all with pip. From the project directory, run the command:
`pip install -r requirements.txt `


## Running the Server

1. Initialize Redis in a terminal window using `redis-server`
2. Start up the flask server in terminal in the project root directory with `python -m flask run`


## Using the App

Once you have your Flask and Redis server running:
1. Go to 127.0.0.1:5000 on your browser. 
2. Click on "Get Started"
3. Enter a session name (anything you like), and select the provider and products you would like to view. 
4. Click "Submit"
5. You can now explore the Employee Directory, Company Data, and Employment Information as you desire. In the directory and employment pages, you can click on employee names to view their details. 
6. When you are done, click "End Session" and your session will be cleared. Feel free to create a new one!

If you have any questions, please reach out to fake-support-email @ example.com