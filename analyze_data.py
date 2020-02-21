


import glob
from datetime import datetime
import pandas as pd


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
    print(fname)
    with open(fname) as fin:
        for line in fin.readlines():
            content.append(process_line(line))

df = pd.DataFrame(content,columns=['date','low','high','open','close','volume'])
df['date'] = pd.to_datetime(df['date'],format='%Y%m%dT')
df.set_index('date',inplace=True)

# plot
fig = df['close'].plot(figsize=(20,10))
fig.figure.savefig('plots/figure.pdf')



