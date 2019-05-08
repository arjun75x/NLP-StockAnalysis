import json
import pandas as pd
import requests
import requests.auth
import praw
import pprint
import textblob
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import numpy as np

#training method
#runs through some training data to find line of best fit
def train():
  # Reddit account data
  my_username = '410project'
  my_password = 'cs410uiuc'
  my_client_id = 'vlFppvzk2DyRpg'
  my_client_secret = 'iFUWIaGBbHpCCskN50o8g-QBAg0'
  my_user_agent = '410client/0.1 by 410project'

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


  #left and right sides of URL
  LEFT_URL = 'https://api.iextrading.com/1.0/stock/'
  RIGHT_URL = '/chart'



  reddit = praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent, username= my_username, password= my_password)


  #x and y data for linear regression
  np_changes = np.array([])
  np_polarity = np.array([])

  data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  table = data[0]



  # goes through each company in the table to collect sentiment vs price change
  for i in range(1, len(table[0])):
    company = table[0][i]
    print(company)
  
    #finding prices
    prices = requests.get(LEFT_URL + company.lower() + RIGHT_URL).json()
    end = prices[len(prices)-1]['close']
    start = prices[0]['close']
    change = (end - start)/start
  
    # calculates the sentiment, throws out outliers, and normalizes it
    score = 0
    count = 0
    for submission in reddit.subreddit('stocks').search(company, time_filter='month'):
      count += 1
      sentiment = textblob.TextBlob(submission.selftext).sentiment
      score += sentiment[0] * sentiment[1]
    


    if count > 0 and score < 2 and score > -2:

      score /= count
      np_changes = np.append(np_changes, np.array([change]), 0)
      np_polarity = np.append(np_polarity, np.array([score]), 0)



  np_changes2 = np_changes.reshape(-1, 1)
  np_polarity2 = np_polarity.reshape(-1, 1)

  #performs linear regression on the data to find the line of best fit
  reg = LinearRegression().fit(np_polarity2, np_changes2)
  paramsToSave = np.array([reg.coef_, reg.intercept_])
  np.save("bestFit.npy", paramsToSave)
  print(paramsToSave)


  #draws plot of datapoints and best fit line with matplotlib
  plt.scatter(np_polarity, np_changes)
  plt.plot([0, 0.5], [reg.intercept_, reg.intercept_ + 0.5*reg.coef_])
  plt.show()







def getWeekScore(company):
  # Reddit account data
  my_username = '410project'
  my_password = 'cs410uiuc'
  my_client_id = 'vlFppvzk2DyRpg'
  my_client_secret = 'iFUWIaGBbHpCCskN50o8g-QBAg0'
  my_user_agent = '410client/0.1 by 410project'

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



  LEFT_URL = 'https://api.iextrading.com/1.0/stock/'
  RIGHT_URL = '/chart'


  count = 0
  score = 0
  reddit = praw.Reddit(client_id= my_client_id, client_secret= my_client_secret, user_agent= my_user_agent, username= my_username, password= my_password)

  for submission in reddit.subreddit('stocks').search(company, time_filter='month'):
    count += 1
    sentiment = textblob.TextBlob(submission.selftext).sentiment
    score += sentiment[0] * sentiment[1]

  if count == 0:
    return None
  score /= count

  return score



if __name__ == "__main__":
  print("")


