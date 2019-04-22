import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import pprint
import requests
import textblob
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from reddit_client import get_client

# Reddit client
reddit = get_client()

company_changes = {}
company_polarity = {}
company_subjectivity = {}

np_changes = np.array([])
np_polarity = np.array([])

fortune500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = fortune500[0]

myTable = ['AMZN', 'GOOGL', 'AMD', 'AAPL', 'NFLX', 'FB', 'MSFT', 'NVDA', 'QCOM', 'TWTR', 'INTC', 'CSCO', 'ADBE', 'IBM', 
'TXN', 'VMW', 'NOW', 'AABA', 'RHT', 'EA', 'TEAM', 'ADSK', 'BB', 'BOX']

LEFT_URL = 'https://api.iextrading.com/1.0/stock/'
RIGHT_URL = '/chart'

for i in range(1, 30):
  company = table[1][i]
  print(company)
  
  #finding prices
  prices = requests.get(LEFT_URL + company.lower() + RIGHT_URL).json()
  end = prices[len(prices)-1]['close']
  start = prices[0]['close']
  change = (end - start)/start
  company_changes[company] = change
  
  #finding polarity and subjectivity
  polarity = 0
  subjectivity = 0
  count = 0
  for submission in reddit.subreddit('stocks').search(company, time_filter='month'):
    count += 1
    sentiment = textblob.TextBlob(submission.selftext).sentiment
    polarity += sentiment[0]
    subjectivity += sentiment[1]
    polarity *= subjectivity

  if count > 0 and polarity < 2 and polarity > -2:

  	polarity /= count
  	company_polarity[company] = polarity
  	company_subjectivity[company] = subjectivity
  	np_changes = np.append(np_changes, np.array([change]), 0)
  	np_polarity = np.append(np_polarity, np.array([polarity]), 0)



np_changes2 = np_changes.reshape(-1, 1)
np_polarity2 = np_polarity.reshape(-1, 1)


print(np_polarity)
print(np_changes)

#poly = PolynomialFeatures(degree=2)
#np_polarity = poly.fit_transform(np_polarity)

reg = LinearRegression().fit(np_polarity2, np_changes2)
print(reg.score(np_polarity2, np_changes2))
print(reg.coef_)
print(reg.intercept_)

plt.scatter(np_polarity, np_changes)
plt.plot([0, 0.5], [reg.intercept_, reg.intercept_ + 0.5*reg.coef_])
plt.show()


