import glob
from datetime import datetime
import pandas as pd
from Trader import Trader

PATTERN = '%Y-%m-%dT%H:%M:%S'

def process_line(line):
    content = line.strip('\n|[|]').split(',')
    for i in range(len(content)):
        content[i] = eval(content[i])
        if i == 0:
            content[i] = datetime.fromtimestamp(content[i]).strftime(PATTERN)
    return content




content = []
for fname in glob.glob('data/*'):
    with open(fname) as fin:
        for line in fin.readlines():
            content.append(process_line(line))

df = pd.DataFrame(content,columns=['date','low','high','open','close','volume'])
df['date'] = pd.to_datetime(df['date'],format='%Y%m%dT%H')
df.set_index('date',inplace=True)
df.sort_index(inplace=True)


res = []
trader = Trader(10000)
for i,price in enumerate(df['open']):
    r = trader.trade((df.index[i],price))
    if r != []: res+=r
    trader.query_portfolio(df.index[i])


fig = df['close'].plot(figsize=(80,15))
for r in res:
    df1 = pd.DataFrame([[r[0],r[1]],[r[2],r[3]]],columns=['date','price'])
    df1['date'] = pd.to_datetime(df1['date'],format='%Y%m%dT')
    df1.set_index('date',inplace=True)

    df1.plot(ax=fig,color='red')
    fig.legend([])

fig.figure.savefig('plots/figure.pdf')



