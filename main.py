import websocket
import requests
import threading
import time
import json
import pymongo
import queue


msg_q = queue.Queue()


def on_message(ws, msg):
    message = json.loads(msg)
    if 'hb' in message:
        pass
    else:
        msg_q.put(message)


if __name__ == '__main__':

    # pairs_to_watch = ['tBTCUSD', 'tETHUSD', 'tBCHUSD']

    pairs_list = ['tBTCUSD', 'tETHUSD', 'tETHBTC']

    db_client = pymongo.MongoClient()
    db = db_client.bitfinex

    state = 'init'

    while True:
        if state == 'init':
            sock_app = websocket.WebSocketApp('wss://api.bitfinex.com/ws/2',
                                              on_message=on_message)
            while not msg_q.empty():
                msg_q.get()
            thread = threading.Thread(target=sock_app.run_forever)
            thread.start()
            while msg_q.empty():
                pass
            msg = msg_q.get()
            if msg['event'] == 'info' and msg['version'] == 2:
                state = 'subscription'
            else:
                raise ValueError('error in init')
        elif state == 'subscription':
            for pair in pairs_list:
                sock_app.send(json.dumps({'event': 'subscribe',
                                          'channel': 'ticker',
                                          'symbol': pair}))
            channels = {}
            state = 'receiving'
            last_time = time.time()
        elif state == 'receiving':
            if time.time() - last_time > 25:
                sock_app.close()
                thread.join()
                state = 'init'
                print('timed out')
            if not msg_q.empty():
                last_time = time.time()
                msg = msg_q.get()
                if type(msg) == dict:
                    if msg['event'] == 'subscribed':
                        channels[msg['chanId']] = msg['symbol']
                    elif msg['event'] == 'info' and msg['code'] == 20051:
                        print(msg)

                        sock_app.close()
                        thread.join()
                        state = 'init'
                    else:
                        raise ValueError('error')
                elif type(msg) == list:
                    for channel in channels:
                        if msg[0] == channel:
                            new_msg = {}
                            new_msg['symbol'] = channels[channel]
                            new_msg['timestamp'] = time.time()
                            new_msg['BID'] = msg[1][0]
                            new_msg['BID_SIZE'] = msg[1][1]
                            new_msg['ASK'] = msg[1][2]
                            new_msg['ASK_SIZE'] = msg[1][3]
                            new_msg['DAILY_CHANGE'] = msg[1][4]
                            new_msg['DAILY_CHANGE_PERC'] = msg[1][5]
                            new_msg['LAST_PRICE'] = msg[1][6]
                            new_msg['VOLUME'] = msg[1][7]
                            new_msg['HIGH'] = msg[1][8]
                            new_msg['LOW'] = msg[1][9]

                            collection = db[channels[channel]]
                            collection.insert_one(new_msg)
                            # print(new_msg)
                else:
                    raise ValueError('unknown type')
            else:
                time.sleep(.1)



