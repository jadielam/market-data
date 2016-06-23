'''
Created on May 29, 2016

@author: jadiel
'''

import sys
import json
import datetime
import time
import gzip
import shutil
import os
from utils import create_tradeking_client
from utils import get_market_time_range
from utils import read_symbols


def main():
    configurationFile = sys.argv[1]
    with open(configurationFile) as f:
        configuration = json.load(f)
    
    tkapi = create_tradeking_client(configuration)
    symbols = read_symbols(configuration)
    print(symbols)
    openingTime, closingTime = get_market_time_range()
    outputFolder = configuration['outputFolder']
    outputFile = str(openingTime.year) + "_" + str(openingTime.month) + "_" + str(openingTime.day) + '_quotes.txt'
    outputPath = os.path.join(outputFolder, outputFile)
    compressedOutputPath = os.path.join(outputFolder, outputFile + ".gz")
    
    #1. Write data to file
    with open(outputPath, "a+") as f:
        while True:
            now = datetime.datetime.now()
            if now >= openingTime and now <= closingTime:
                try:
                    start = time.time()
                    quotesPayload = tkapi.market.quotes(symbols)
                    end = time.time()
                    delta = end - start
                    quotesList = quotesPayload['response']['quotes']['quote']
                    for quote in quotesList:
                        quoteText = json.dumps(quote)
                        f.write(quoteText)
                        f.write('\n')
                
                    time.sleep(max(0, 1 - delta))
                except Exception as e:
                    print(now)
                    print(e)
            elif now > closingTime:
                break
    
    #2. Compress file
    with open(outputPath, 'rb') as f_in, gzip.open(compressedOutputPath, "wb+") as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    #3. Remove original file
    os.remove(outputPath)
    
    

if __name__ == '__main__':
    main()