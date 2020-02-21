

import os
import cbpro
import numpy as np
from datetime import datetime,timedelta

PATTERN = '%Y-%m-%dT%H:%M:%S'

pc = cbpro.PublicClient()

startDate = '2016-01-01T00:00:00'
while True:
    endDate = (datetime.strptime(startDate, PATTERN) + timedelta(days=200)).strftime(PATTERN)
    print(startDate,endDate)
    fname = 'data/%s_%s' % (startDate,endDate)
    if not os.path.isfile(fname):
        rates = pc.get_product_historic_rates('BTC-EUR', granularity=86400, start=startDate, end=endDate)
        if len(rates) > 200:
            with open(fname,'w') as fout:
                for rate in rates:
                    fout.write("%s\n" % rate)
    startDate = endDate
    if endDate > '2020-02-19T00:00:00':
        break



