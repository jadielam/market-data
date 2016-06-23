'''
Created on May 31, 2016

@author: jadiel
'''
import sys
import json
import datetime
import os
from utils import create_tradeking_client
from utils import read_symbols
from utils import get_market_time_range

def main():
    configurationFile = sys.argv[1]
    with open(configurationFile) as f:
        configuration = json.load(f)
    
    tkapi = create_tradeking_client(configuration)
    symbols = read_symbols(configuration)
    print(symbols)
    openingTime, closingTime = get_market_time_range()
    outputFolder = configuration['outputFolder']
    outputFile = str(openingTime.year) + "_" + str(openingTime.month) + "_" + str(openingTime.day) + '_news.txt'
    outputPath = os.path.join(outputFolder, outputFile)
    compressedOutputPath = os.path.join(outputFolder, outputFile + ".gz")
    
    news_ids = dict()
    with open(outputPath, "a+") as f:
        while True:
            now = datetime.datetime.now()
            if now <= closingTime:
                try:
                    start = 1
                except:
                    pass
            break
    
    
    keywords = []
    response = tkapi.market.news.search(symbols = symbols, maxhits = 50)
    print(len(response))
    print(response)
    
    id1 = response[0]['id']
    news = tkapi.market.news.article(id)
    print(news)
    
if __name__=="__main__":
    main()