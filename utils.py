'''
Created on May 31, 2016

@author: jadiel
'''
import csv
import tradeking
import datetime

def get_market_time_range():
    today = datetime.datetime.today()
    openingTime = datetime.datetime(today.year, today.month, today.day, 8, 30, 0)
    closingTime = datetime.datetime(today.year, today.month, today.day, 16, 0, 0)
    return openingTime, closingTime

def create_tradeking_client(configuration):
    tkapi = tradeking.TradeKing(consumer_key=configuration['consumerKey'],
                                consumer_secret=configuration['consumerSecret'],
                                oauth_token=configuration['oauthToken'],
                                oauth_secret=configuration['oauthTokenSecret'])
    return tkapi

def read_symbols(configuration):
    symbolsFiles = configuration['symbolsFiles'].split(",")
    symbols = list()
    symbolsMap = dict()
    for symbolsFile in symbolsFiles:
        with open(symbolsFile) as f:
            csvreader = csv.reader(f, delimiter=",")
            count = 0
            for row in csvreader:
                if count > 0:
                    symbol = row[0]
                    if not symbol in symbolsMap:
                        symbols.append(row[0])
                        symbolsMap[symbol] = 1
                count = count + 1
    return symbols