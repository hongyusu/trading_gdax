# -*- coding: utf-8 -*-
# ------------------------------------------------+
#                                                 |
#  TRADING HUB                                    |
#                                                 |
#                                                 |
# ------------------------------------------------+
import gdax
import re
import engine
import time
import logging
logging.basicConfig(format='%(asctime)s %(name)15s %(levelname)10s:%(message)s')
logger = logging.getLogger('gdax.hub')
logger.setLevel(logging.INFO)


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

while True:
    buy_order = engine.generate_buy_order(ac, pc)  
    sell_order = engine.generate_sell_order(ac, pc)  




#print(ac.get_accounts())
#print(ac.get_orders())
#print(pc.get_product_trades(product_id='BTC-EUR'))
#print(pc.get_product_historic_rates('BTC-EUR', granularity=10000))
#print(pc.get_product_24hr_stats('BTC-EUR'))
#print(pc.get_time())
#print(pc.get_currencies())
#print(pc.get_product_ticker(product_id='BTC-EUR'))
#print(pc.get_products())
#print(pc.get_product_order_book('BTC-EUR',level=1))
#print(pc.get_product_order_book('BTC-EUR',level=3))
