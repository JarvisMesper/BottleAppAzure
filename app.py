"""
This script runs the application using a development server.
"""

import bottle
import os
import sys

# routes contains the HTTP handlers for our server and must be imported.
from bottle import Bottle, request, debug, route

from actions import forecast
from actions import openfood

import requests
from wit import Wit

terminal_mode = False

app = Bottle()

WIT_TOKEN = os.environ.get('WIT_TOKEN')

if not terminal_mode:
    # Messenger API parameters
    FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
    # A user secret to verify webhook get request.
    FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

    # Setup Bottle Server
    debug(True)

    # Facebook Messenger GET Webhook
    @app.get('/webhook')
    def messenger_webhook():
        """
        A webhook to return a challenge
        """
        verify_token = request.query.get('hub.verify_token')
        print(verify_token)

        # check whether the verify tokens match
        if verify_token == FB_VERIFY_TOKEN:
            # respond with the challenge to confirm
            challenge = request.query.get('hub.challenge')
            return challenge
        else:
            return 'Invalid Request or Verification Token'


    # Facebook Messenger POST Webhook
    @app.post('/webhook')
    def messenger_post():
        """
        Handler for webhook (currently for postback and messages)
        """
        data = request.json
        if data['object'] == 'page':
            for entry in data['entry']:
                # get all the messages
                messages = entry['messaging']
                if messages[0]:
                    # Get the first message
                    message = messages[0]
                    # Yay! We got a new message!
                    # We retrieve the Facebook user ID of the sender
                    fb_id = message['sender']['id']
                    # We retrieve the message content
                    text = message['message']['text']
                    # Let's forward the message to the Wit.ai Bot Engine
                    # We handle the response in the function send()
                    client.run_actions(session_id=fb_id, message=text)
        else:
            # Returned another event
            return 'Received Different Event'
        return None



@app.route('/')
def index():
    """Renders the home page."""
    return "Hello World"

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return app

def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


def send(request, response):
    """
    Sender function
    """
    print('--- send called ---')
    #print(request)
    #print(response)

    if terminal_mode:
        print(response['text'])
    else:
        # We use the fb_id as equal to session_id
        fb_id = request['session_id']
        text = response['text']
        # send message
        fb_message(fb_id, text)


actions = {
    'send': send,
    'getForecast': forecast.get_forecast,
    #'getOpenFoodInfo': openfood.getOpenFoodInfo,
}

client = Wit(access_token=WIT_TOKEN, actions=actions)


if __name__ == '__main__':

    if terminal_mode:
        client.interactive()
    else:
        # Run Server
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
        HOST = os.environ.get('SERVER_HOST', 'localhost')
        try:
            PORT = int(os.environ.get('SERVER_PORT', '5555'))
        except ValueError:
            PORT = 5555

        # Starts a local test server.
        app.run(server='wsgiref', host=HOST, port=PORT)