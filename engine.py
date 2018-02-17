# -*- coding: utf-8 -*-
# ------------------------------------------------+
#                                                 |
#  TRADING ENGINE                                 |
#                                                 |
#                                                 |
# ------------------------------------------------+
import logging
import traceback
import time
import sys
from time import time
from time import sleep
import re
import gdax
import random

logging.basicConfig(format='%(asctime)s %(name)15s %(levelname)10s:%(message)s')
logger = logging.getLogger('gdax.engine')
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

# TODO: read from configuration file
LIMIT_EURO = 10
LIMIT_VOLUME = 1e-3 
PRODUCT = 'BTC-EUR'
DELTA_BUY_PRICE = 15
DELTA_SELL_PRICE = 50

# global variables 
price_pool = [0]*10


# initialization
configs = {}
for line in open('./utils/configs_prod.ini'):
    if line.startswith('APIKEY'):
        APIKEY = re.sub('^APIKEY=','',line.strip())
    if line.startswith('APISECRET'):
        APISECRET = re.sub('^APISECRET=','',line.strip())
    if line.startswith('PASSPHRASE'):
        PASSPHRASE = re.sub('^PASSPHRASE=','',line.strip())

# public client
pc = gdax.PublicClient()
# authorized client
ac = gdax.AuthenticatedClient(APIKEY, APISECRET, PASSPHRASE)

# all buy order 
pending_buy_order = {} 
order_info = ac.get_orders()[0]
for order in order_info:
    if order['side'] == 'buy':
        pending_buy_order[order['id']] = eval(order['price'])

last_buy_price = 0

def buy_order_from_pp():
    global price_pool
    logger.debug("<--- {:8.2f} --  {} -- {:8.2f} -- {} -- {:8.2f} -- {} -- {:8.2f}".format(
        price_pool[-1], 
        price_pool[-1] < price_pool[-2], 
        price_pool[-2], 
        price_pool[-2] < price_pool[-3], 
        price_pool[-3], 
        price_pool[-3] < price_pool[-4], 
        price_pool[-4]))

    try:
        if price_pool[-1] < price_pool[-2] and price_pool[-2] < price_pool[-3] and price_pool[-3] < price_pool[-4]:
            return True
        else:
            return False

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')

def generate_buy_order(n):
    global last_buy_price
    global LIMIT_EURO
    global DELTA_BUY_PRICE

    try:
        sleep(0.5)
        ask_price_list = pc.get_product_order_book(PRODUCT,level=1)['asks']
        price_to_buy, _, _ = ask_price_list[0]
        price_to_buy = eval(price_to_buy)
        price_pool.append(price_to_buy)
        price_to_buy -= 0.1

        if abs(last_buy_price - price_to_buy) > DELTA_BUY_PRICE and buy_order_from_pp():
            euro_cost = price_to_buy * LIMIT_VOLUME 
            account_info = ac.get_account('e1ce1c04-208f-4e18-8062-52961c9c7eb7')
            if euro_cost < account_info['available'] - LIMIT_EURO:
                # buy
                buy_order = ac.buy(price='{}'.format(price_to_buy), size=LIMIT_VOLUME,product_id=PRODUCT)
                print(buy_order)
                pending_buy_order[buy_order['id']] = price_to_buy
                logger.info('{:6s} ORDER AT {:.8f} WHEN BALANCE {:.8f} AVAILABLE {:.8f} HOLD {:.8f}'.format('BUY', price_to_buy, account_info['balance'], account_info['available'], account_info['hold']))
                last_buy_price = price_to_buy
                price_pool.append(-1)
                sleep(3)

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')

def generate_sell_order():
    try:
        if len(pending_buy_order.keys()) == 0:
            return
        to_remove = []
        for pending_buy_order_id,price_to_sell in pending_buy_order.items():
            price_to_sell += DELTA_SELL_PRICE
            order_info = ac.get_fills(order_id=pending_buy_order_id)[0]
            if len(order_info) > 0:
                sell_order = ac.sell(price='{:.2f}'.format(price_to_sell),size='{}'.format(LIMIT_VOLUME),product_id=PRODUCT)
                print(sell_order)
                to_remove.append(pending_buy_order_id)
                logger.info('{:6s} ORDER AT {:.8f}'.format('SELL', price_to_sell))
        for pending_buy_order_id in to_remove:
            pending_buy_order.pop(pending_buy_order_id, None)

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')
    pass



