#!/usr/bin/python3
import requests
import pymongo
import time


if __name__ == '__main__':
    pairs_details = requests.get('https://api.bitfinex.com/v1/symbols_details').json()

    url = 'https://api.bitfinex.com/v2/tickers?symbols='
    for pair in pairs_details:
        url = url + 't' + pair['pair'].upper() + ','

    all_tickers = requests.get(url).json()

    tickers_dict = {}
    for ticker in all_tickers:
        tmp_dict = dict()
        tmp_dict['SYMBOL'] = ticker[0]
        tmp_dict['BID'] = ticker[1]
        tmp_dict['BID_SIZE'] = ticker[2]
        tmp_dict['ASK'] = ticker[3]
        tmp_dict['ASK_SIZE'] = ticker[4]
        tmp_dict['DAILY_CHANGE'] = ticker[5]
        tmp_dict['DAILY_CHANGE_PERC'] = ticker[6]
        tmp_dict['LAST_PRICE'] = ticker[7]
        tmp_dict['VOLUME'] = ticker[8]
        tmp_dict['HIGH'] = ticker[9]
        tmp_dict['LOW'] = ticker[10]

        for tick in all_tickers:
            if tick[0] == ticker[0][0:4] + 'USD':
                tmp_dict['VOLUME_USD'] = ticker[8] * tick[7]

        tickers_dict[ticker[0]] = tmp_dict

    tickers_dict['timestamp'] = time.time()
    # db_client = pymongo.MongoClient()
    # db = db_client.bitfinex
    # collection = db['overview']
    # collection.insert_one(tickers_dict)


