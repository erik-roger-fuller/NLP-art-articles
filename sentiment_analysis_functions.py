import numpy as np
from numpy import linspace, loadtxt, ones, convolve
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.lines as ln
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange , date2num
import json
import os
import nltk
from nltk import RegexpTokenizer
import re
from datetime import datetime
import time
from scipy.signal import savgol_filter

def polarity_analysis(data):
    # polarity analysis of paras with textblob
    pol = lambda x: TextBlob(x).sentiment.polarity
    sub = lambda x: TextBlob(x).sentiment.subjectivity
    data['polarity'] = data['para'].apply(pol)
    data['subjectivity'] = data['para'].apply(sub)
    return data

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def timeplot_sentiment(data , sentiment, path):
    """plot changes in polarity over time
    sentiment = subjectivity or polarity"""
    data.sort_values(by=['pubtime'], inplace=True)
    data = polarity_analysis(data)
    plt.rcParams['figure.figsize'] = [12, 8]
    fig, ax = plt.subplots()
    xs, ys, yhats = [], [], []

    for index, para in enumerate(data.index):
        # pubdate_c = plt_dates.date2num(pubtime)
        xinput = data.pubtime.loc[para]
        x = date2num(xinput)
        xs.append(x)
        if "pol" in sentiment:
            y = data.polarity.loc[para]
            flag = "Polarity"
        else:
            y = data.subjectivity.loc[para]
            flag = "Subjectivity"
        ys.append(y)
        # yhat = movingaverage(index, 10)# yhats.append(yhat)# print([y, yhat])

    # print(yhats)
    yhat = savgol_filter(ys, 201, 3)
    yhat = list(yhat)
    # print(yhat)

    sample = len(ys)
    ax.set_title(f'{path} Sentiment {flag} Analysis ', fontsize=20) #\n with wordcount > {count}
    ax.set_xlabel(f'Change over time.\n N={sample}', fontsize=15)
    ax.set_ylabel('<-- Factlike                 Opinionated -->', fontsize=15)
    ax.tick_params(axis="x", rotation=30)
    # set as years months x axis   # ax.xaxis.set_minor_locator(MonthLocator())# ax.xaxis.set_minor_formatter(DateFormatter('%m'))
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))

    ax.fmt_xdata = DateFormatter('%Y-%m')
    fig.autofmt_xdate()
    ax.plot(xs, yhat, color='red')
    ax.scatter(xs, ys, color='green', s=1)
    plt.show()


# round to nearest years.
# datemin = np.datetime64(data['pubtime'][0], 'Y')
# datemax = np.datetime64(data['pubtime'][-1], 'Y') + np.timedelta64(1, 'Y')
# ax.set_xlim(datemin, datemax)