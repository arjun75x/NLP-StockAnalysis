from tkinter import *

import pandas as pd
import numpy as np
import pricePrediction


fortune500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = fortune500[0]



#Setting up ticker to company dictionary
ticker_company_dict = {}
for i in range(1,500):
    ticker = table[0][i]
    company = table[1][i]
    ticker_company_dict[ticker] = company


#Start of the UI
window = Tk()
window.title("Stock Predictions based on Sentiment Analysis")

window.geometry('800x300')

lbl = Label(window, text="Enter a Stock Ticker")

lbl.grid(column=0, row=0)

txt = Entry(window,width=10)

txt.grid(column=1, row=3)

output = Entry(window,width=10)
output.grid(column=1, row=4)

#button clicked to start analysis on given company
def clicked():
    ticker = txt.get().upper()
    if ticker in ticker_company_dict:
        company = ticker_company_dict[ticker]
        res = "Performing Sentiment Analysis for " + company + '(' + ticker + ')'
        lbl.configure(text= res)


        
        params = np.load("bestFit.npy")
        
        score = pricePrediction.getWeekScore(ticker)
        if score != None:
            prediction = (params[0][0] * score + params[1][0])
            temp = output.get()
            output.delete(0, len(temp))
            output.insert(0, prediction)
            print(prediction)
        else:
            temp = output.get()
            output.delete(0, len(temp))
            output.insert(0, prediction)
            print('No Data')

    else:
        res = "Invalid Ticker Symbol, Please Try Entering Again"
        lbl.configure(text= res)


#choices for popular stocks to analyze
companyLabel = Label(window, text="Choose A Popular Company")
companyLabel.grid(column=0, row=10)
def APPLE():
    txt.delete(0, END)
    txt.insert(0,"AAPL")
    clicked()

def FACEBOOK():

    txt.delete(0, END)
    txt.insert(0,"FB")
    clicked()

def GOOGLE():

    txt.delete(0, END)
    txt.insert(0,"GOOG")
    clicked()

def NVIDIA():

    txt.delete(0, END)
    txt.insert(0,"NVDA")
    clicked()


def AMAZON():

    txt.delete(0, END)
    txt.insert(0,"AMZN")
    clicked()

def reTrain():
    pricePrediction.train()

#fixing positions of buttons
btn = Button(window, text="Analyze", command=clicked)

btn.grid(column=2, row=3)

applebtn = Button(window, text="APPLE", command=APPLE)
applebtn.grid(column=0, row=15)

fbbtn = Button(window, text="FACEBOOK", command=FACEBOOK)
fbbtn.grid(column=0, row=11)



googlebtn = Button(window, text="GOOGLE", command=GOOGLE)
googlebtn.grid(column=0, row=12)

amazonbtn = Button(window, text="AMAZON", command=AMAZON)
amazonbtn.grid(column=0, row=13)

nvdiabtn = Button(window, text="NVIDIA", command=NVIDIA)
nvdiabtn.grid(column=0, row=14)

trainbtn = Button(window, text="Train", command=reTrain)
trainbtn.grid(column=10, row=3)



window.mainloop()
