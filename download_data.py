

import os
import cbpro
import numpy as np
from datetime import datetime,timedelta
import time

PATTERN = '%Y-%m-%dT%H:%M:%S'

pc = cbpro.PublicClient()

startDate = '2016-01-01T00:00:00'
while True:
    endDate = (datetime.strptime(startDate, PATTERN) + timedelta(hours=200)).strftime(PATTERN)
    fname = 'data/%s_%s' % (startDate,endDate)
    if not os.path.isfile(fname):
        rates = pc.get_product_historic_rates('BTC-EUR', granularity=3600, start=startDate, end=endDate)
        print(startDate,endDate,fname,len(rates))
        if len(rates) >= 190:
            time.sleep(2)
            with open(fname,'w') as fout:
                for rate in rates:
                    fout.write("%s\n" % rate)
    startDate = endDate
    if endDate > '2020-02-20T00:00:00':
        break



