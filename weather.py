import os
import time
import json
import requests
from requests_oauthlib import OAuth1Session

# Twitter API credentials
consumer_key = 'YOUR KEY'
consumer_secret = 'YOUR SECRET'

# Weather API credentials
weather_api_key = "YOUR KEY"
location = "Berlin" 

# Check if we already have access tokens saved
tokens_file = 'twitter_tokens.json'
if os.path.exists(tokens_file):
    with open(tokens_file, 'r') as file:
        tokens = json.load(file)
    access_token = tokens['access_token']
    access_token_secret = tokens['access_token_secret']
else:
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Save the obtained tokens to a file for future use
    with open('twitter_tokens.json', 'w') as file:
        json.dump({
            'access_token': access_token,
            'access_token_secret': access_token_secret
        }, file)


# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)


# Function to get the current weather
def get_weather():
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp_celsius = round(data["main"]["temp"] - 273.15, 2)
        condition = data["weather"][0]["description"].capitalize()
        return f"🌤 Weather in {location}: {condition}, {temp_celsius}°C."
    else:
        return "Error retrieving weather data."

# Function to post weather updates on Twitter
def post_weather():
    weather_text = get_weather()
    
     # Update the OAuth session if needed (code from your OAuth setup)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": weather_text}
    )

    if response.status_code != 201:
        print("Error posting tweet:", response.text)
    else:
        print("Tweet posted:", weather_text)

# Run the bot every 6 hours
def run_bot():
    while True:
        post_weather()
        time.sleep(21600)  

run_bot()