# -*- coding: utf-8 -*-
# ------------------------------------------------+
#                                                 |
#  TRADING                                        |
#                                                 |
#                                                 |
# ------------------------------------------------+
import logging
logging.basicConfig(format='%(asctime)s %(filename)15s %(funcName)20s %(levelname)s:%(message)s')
logger = logging.getLogger('gdax.logger')
logger.setLevel(logging.INFO)

LIMIT_INVEST = 10
LIMIT_VOLUME = 1e-5 
HAVE = []

def generate_buy_order(ac, pc):
    
    order = {
            'type': 'buy',
            'execuate':False,
            'volume':0,
            'price':0
            }

    global LIMIT_INVEST

    try:
        order_book = pc.get_product_order_book('BTC-EUR',level=1)
        ask_price_list = order_book['asks']
        price, volume, unit  = ask_price_list[0]
        price, volume = eval(price), eval(volume)

        # logic
        cost_euro = price * LIMIT_VOLUME 
        if not price in HAVE and cost_euro < LIMIT_INVEST:
            LIMIT_INVEST -= cost_euro
            # make order
            order = {
                    'type': 'buy',
                    'execuate':True,
                    'volume':LIMIT_VOLUME,
                    'price':price
                    }
            HAVE.append(price)
            logger.info('BUY  AT {:.8f}'.format(price))

    except Exception as e:
        traceback.print_exc()

    logger.info('INFO EURO {:.8f} BTC {:.8f} total {:.8f}'.format(LIMIT_INVEST, sum(HAVE)*LIMIT_VOLUME, LIMIT_INVEST + sum(HAVE)*LIMIT_VOLUME))
    return order

def generate_sell_order(ac, pc):
    
    order = {
            'type': 'sell',
            'execuate':False,
            'volume':0,
            'price':0
            }

    global LIMIT_INVEST

    try:
        order_book = pc.get_product_order_book('BTC-EUR',level=1)
        ask_price_list = order_book['bids']
        price, volume, unit  = ask_price_list[0]
        price, volume = eval(price), eval(volume)

        if price > min(HAVE):
            # make order 
            order = {
                    'type': 'sell',
                    'execuate':True,
                    'volume':LIMIT_VOLUME,
                    'price':price
                }
            logger.info('SELL FROM {:.8f} TO {:.8f}'.format(min(HAVE),price))
            HAVE.remove(min(HAVE))
            get_euro = price * LIMIT_VOLUME
            LIMIT_INVEST+=get_euro

    except Exception as e:
        traceback.print_exc()

    logger.info('INFO EURO {:.8f} BTC {:.8f} total {:.8f}'.format(LIMIT_INVEST, sum(HAVE)*LIMIT_VOLUME, LIMIT_INVEST + sum(HAVE)*LIMIT_VOLUME))
    return order

