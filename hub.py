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
from time import sleep
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

n = 0
while True:
    n+=1
    engine.generate_buy_order(ac, pc, n)  
    engine.generate_sell_order(ac, pc)
    sleep(1)

