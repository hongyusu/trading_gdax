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
price_pool = []


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
        print(price_pool[-3:])
        if price_pool[-1] < price_pool[2] and pirce_pool[-2] < price_pool[-3]:
            return True
        else:
            return False
    except:
        return False 

def generate_buy_order(ac, pc, n):

    global price_pool

    try:
        order_book = pc.get_product_order_book(PRODUCT,level=1)
        ask_price_list = order_book['asks']
        price_to_buy, _, _ = ask_price_list[0]
        price_pool.append(price_to_buy)

        if buy_order_from_pp():
            price_to_buy = eval(price_to_buy) - 0.01
            euro_cost = price_to_buy * LIMIT_VOLUME 
            if euro_cost < euro_pool:
                logger.info('{:6s} ORDER AT {:.8f}'.format('BUY', price_to_buy))

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')



