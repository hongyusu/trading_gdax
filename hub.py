# -*- coding: utf-8 -*-
# ------------------------------------------------+
#                                                 |
#  TRADING HUB                                    |
#                                                 |
#                                                 |
# ------------------------------------------------+
import engine
from time import sleep
import logging
logging.basicConfig(format='%(asctime)s %(name)15s %(levelname)10s:%(message)s')
logger = logging.getLogger('gdax.hub')
logger.setLevel(logging.INFO)


n = 0
while True:
    n+=1
    engine.generate_buy_order(n)  
    engine.generate_sell_order()

