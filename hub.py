# -*- coding: utf-8 -*-
# ------------------------------------------------+
#                                                 |
#  TRADING                                        |
#                                                 |
#                                                 |
# ------------------------------------------------+
import gdax
import re
import decision
import time
import logging
logging.basicConfig(format='%(asctime)s %(filename)15s %(funcName)20s %(levelname)s:%(message)s')
logger = logging.getLogger('gdax.logger')
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
#ac = gdax.AuthenticatedClient(APIKEY, APISECRET, PASSPHRASE, api_url="https://api-public.sandbox.gdax.com")
ac = gdax.AuthenticatedClient(APIKEY, APISECRET, PASSPHRASE)

while True:
    buy_order = decision.generate_buy_order(ac, pc)  
    sell_order = decision.generate_sell_order(ac, pc)  
    time.sleep(2)

#    print(buy_order)
#    print(sell_order)






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
