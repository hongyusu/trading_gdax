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
START_EURO = 10
LIMIT_VOLUME = 1e-4 
BUY_DELAY_FACTOR = 2
BUY_MAX_DELAY = 16

# global variables 
euro_pool = START_EURO 
btc_price_pool = []
buy_last_price = sys.maxsize
buy_delay_second = 1
buy_next_ts = time()


def log_current_status(current_price): 
    '''
    log current status
    '''
    bc_cost = sum(btc_price_pool) * LIMIT_VOLUME 
    bc_value = len(btc_price_pool) * LIMIT_VOLUME * current_price
    bc_profit = bc_value - bc_cost
    profit = bc_value + euro_pool - START_EURO

    logger.info('PRICE {:.8f} EURO_REMAIN {:.8f} BTC_COST {:.8f} BTC_VALUE {:.8f} BTC_PROFIT {:.8f} PROFIT {:.8f}'.format(
        current_price,
        euro_pool, 
        bc_cost,
        bc_value,
        bc_profit,
        profit
        ))

def generate_buy_order(ac, pc):

    global euro_pool
    global buy_next_ts
    global buy_last_price
    global buy_delay_second
    global btc_price_pool

    order = {
            'type': 'buy',
            'execuate': False,
            'volume': 0,
            'price': 0
            }

    try:
        buy_current_ts = time()

        # GET: price, volume, potential cost
        order_book = pc.get_product_order_book('BTC-EUR',level=1)
        ask_price_list = order_book['asks']
        price, volume, unit  = ask_price_list[0]
        price, volume = eval(price), eval(volume)
        euro_cost = price * LIMIT_VOLUME 

        # MAKE: buy suggestion 
        if len(btc_price_pool) == 0 or \
                not price in btc_price_pool \
                and euro_cost < euro_pool \
                and time() > buy_next_ts:
            order = {
                    'type': 'buy',
                    'execuate': True,
                    'volume': LIMIT_VOLUME,
                    'price': price
                    }
            euro_pool -= euro_cost
            btc_price_pool.append(price)

            # next buy time
            if price < buy_last_price:
                buy_delay_second *= BUY_DELAY_FACTOR
            else:
                buy_delay_second /= BUY_DELAY_FACTOR
            buy_delay_second = max(1,buy_delay_second)
            buy_delay_second = min(BUY_MAX_DELAY, buy_delay_second)

            buy_last_price = price
            buy_next_ts += buy_delay_second

            logger.info('{:6s} ORDER AT {:.8f} FREEZE {} second'.format('BUY', price, buy_delay_second))

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')

    return order

def generate_sell_order(ac, pc):
    
    global euro_pool

    order = {
            'type': 'sell',
            'execuate': False,
            'volume': 0,
            'price': 0
            }

    try:
        # GET: price, volume
        order_book = pc.get_product_order_book('BTC-EUR',level=1)
        ask_price_list = order_book['bids']
        price, volume, unit  = ask_price_list[0]
        price, volume = eval(price), eval(volume)

        if price > min(btc_price_pool):
            # make order 
            order = {
                    'type': 'sell',
                    'execuate': True,
                    'volume': LIMIT_VOLUME,
                    'price': price
                }
            logger.info('{:6s} ORDER FROM {:.8f} TO {:.8f}'.format('SELL', min(btc_price_pool), price))
            btc_price_pool.remove(min(btc_price_pool))
            euro_profit = price * LIMIT_VOLUME
            euro_pool += euro_profit
        log_current_status(price)

    except Exception as e:
        logger.critical('--------------------')
        traceback.print_exc()
        logger.critical('--------------------')

    sleep(1.5)

    return order

