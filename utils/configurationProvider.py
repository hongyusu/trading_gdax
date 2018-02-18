# -*- coding: utf-8 -*-
# ------------------------------------------------+
#                                                 |
# trading                                         |
#                                                 |
#                                                 |
# ------------------------------------------------+
import configparser
import os
config = configparser.ConfigParser()

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

default_path = os.path.join(__location__, 'configs/config.ini')

CONFIG_FILE = os.environ.get('CONFIG_FILE', default_path)

config.read(CONFIG_FILE)


def get_configs():
    # GDAX_ENV can be set to DEFAULT, LOCAL or DOCKER now

    currentenvironment = os.environ.get('GDAX_ENV','DEFAULT')
    params = config[currentenvironment.upper()]

    API_KEY           = os.environ.get('API_KEY',params.get('API_KEY'))
    API_SECRET        = os.environ.get('API_SECRET',params.get('API_SECRET'))
    API_PASSPHRASE    = os.environ.get('API_PASSPHRASE',params.get('API_PASSPHRASE'))
    EURO_ACCOUNT      = os.environ.get('EURO_ACCOUNT',params.get('EURO_ACCOUNT'))
    LIMIT_EURO        = os.environ.get('LIMIT_EURO',params.get('LIMIT_EURO'))
    LIMIT_VOLUME      = os.environ.get('LIMIT_VOLUME',params.get('LIMIT_VOLUME'))
    PRODUCT_NAME      = os.environ.get('PRODUCT_NAME',params.get('PRODUCT_NAME'))
    DELTA_BUY_PRICE   = os.environ.get('DELTA_BUY_PRICE',params.get('DELTA_BUY_PRICE'))
    DELTA_SELL_PRICE  = os.environ.get('DELTA_SELL_PRICE',params.get('DELTA_SELL_PRICE'))
    PRICE_SENSITIVITY = os.environ.get('PRICE_SENSITIVITY',params.get('PRICE_SENSITIVITY'))

    return {
        "API_KEY":           API_KEY,
        "API_SECRET":        API_SECRET,
        "API_PASSPHRASE":    API_PASSPHRASE,
        "EURO_ACCOUNT":      EURO_ACCOUNT,
        "LIMIT_EURO":        float(LIMIT_EURO),
        "LIMIT_VOLUME":      float(LIMIT_VOLUME),
        "PRODUCT_NAME":      PRODUCT_NAME,
        "DELTA_BUY_PRICE":   float(DELTA_BUY_PRICE),
        "DELTA_SELL_PRICE":  float(DELTA_SELL_PRICE),
        "PRICE_SENSITIVITY": float(PRICE_SENSITIVITY),
    }
