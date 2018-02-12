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

logging.basicConfig(format='%(asctime)s %(name)15s %(levelname)10s:%(message)s')
logger = logging.getLogger('gdax.engine')
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

# TODO: read from configuration file
LIMIT_EURO = 10
LIMIT_VOLUME = 1e-3 
BUY_ORDER_DELAY_FACTOR = 2
BUY_ORDER_RECOVER_FACTOR = 3
BUY_ORDER_MAX_DELAY_SEC = 128
PRODUCT = 'BTC-EUR'

# global variables 
euro_pool = LIMIT_EURO 
price_pool = [10e10]*10
order_book = []


#def log_current_status(current_price): 
#    '''
#    log current status
#    '''
#    bc_cost = sum(btc_price_pool) * LIMIT_VOLUME 
#    bc_value = len(btc_price_pool) * LIMIT_VOLUME * current_price
#    bc_profit = bc_value - bc_cost
#    profit = bc_value + euro_pool - LIMIT_EURO
#    btc_price_pool_min = min(btc_price_pool)
#
#    logger.info('PRICE {:.3f} MY {:.3f} EURO_REMAIN {:.8f} COIN_COST {:.8f} COIN_VALUE {:.8f} COIN_PROFIT {:.6f} PROFIT {:.6f}'.format(
#        current_price,
#        btc_price_pool_min,
#        euro_pool, 
#        bc_cost,
#        bc_value,
#        bc_profit,
#        profit
#        ))


def buy_order_from_pp():
    global price_pool
    try:
        if price_pool[-1] < price_pool[2] and price_pool[-2] < price_pool[-3]:
            return True
        else:
            return False
    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')

def generate_buy_order(ac, pc, n):

    global price_pool
    global order_book

    try:
#        ask_price_list = pc.get_product_order_book(PRODUCT,level=1)['asks']
#        price_to_buy, _, _ = ask_price_list[0]
#        price_to_buy = eval(price_to_buy)
        price_to_buy = list(range(100))[-n-1]
        price_pool.append(price_to_buy)

        if buy_order_from_pp():
            price_to_buy -= 0.01
            euro_cost = price_to_buy * LIMIT_VOLUME 
            euro_pool = eval(ac.get_account('e1ce1c04-208f-4e18-8062-52961c9c7eb7')['balance'])
            if euro_cost < euro_pool:
                # buy
                #buy_order = ac.buy(price='{}'.format(price_to_buy), size=LIMIT_VOLUME,product_id=PRODUCT)
                order = {'id':'53a88d80-f55a-4ea7-a3b9-946f79b9685f'}
                order_book.append(order['id'])
                logger.info('{:6s} ORDER AT {:.8f} WITH {:.8f}'.format('BUY', price_to_buy, euro_pool))

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')

def generate_sell_order(ac, pc):
    global order_book

    if len(order_book) == 0:
        return
    fills = ac.get_fills()
    try:
        for order in fills[0]:
            if order['order_id'] == order_book[-1]:

                price_to_sell = eval(order['price']) + 10
                # sell
                sell_order = ac.sell(price='{}'.format(price_to_sell),size=LIMIT_VOLUME,product_id=PRODUCT)
                if 'id' in sell_order:
                    order_bool.remove(order_book[-1])
                    logger.info('{:6s} ORDER AT {:.8f} WITH {:.8f}'.format('SELL', price_to_sell, euro_pool))
    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')
    pass



