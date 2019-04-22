import requests
import requests.auth
import praw

# Reddit account data
my_username = '410project'
my_password = 'cs410uiuc'
my_client_id = 'vlFppvzk2DyRpg'
my_client_secret = 'iFUWIaGBbHpCCskN50o8g-QBAg0'
my_user_agent = '410client/0.1 by 410project'

def initialize_client():
    # Acquire Token
    client_auth = requests.auth.HTTPBasicAuth(my_client_id, my_client_secret)
    post_data = {"grant_type": "password", "username": my_username, "password": my_password}
    headers = {"User-Agent": my_user_agent}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    token = response.json()

    # Use Token
    headers = {"Authorization": "bearer {t}".format(t = token['access_token']), "User-Agent": my_user_agent}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    user_data = response.json()

def get_client():
    initialize_client()
    return praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent, username= my_username, password= my_password)