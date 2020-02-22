

class GridTrade:
    def __init__(self, deposite, memory=10):
        self.portfolio = {'cash':deposite, 'value':0, 'prod':[]}
        self.memory = [0]*10
        self.MIN_AMOUNT = 0.001
        self.BUY_THRESHOLD = 0.1
        self.BUY_TOLERANCE = 0.03
        self.BUY_POWER = 0.1
        self.SELL_THRESHOLD = 0.05

    def query_portfolio(self,date):
        print(date, self.portfolio['cash'], self.portfolio['value'])
        for item in self.portfolio['prod']:
            #print(item)
            pass
        pass

    def trade(self, info):
        date,price = info
        self.__grid_buy(date,price)
        self.__grid_sell(price)
        self.__update(price)

    def __update(self, price):
        new_record = price
        self.memory.append(new_record)
        self.memory.pop(0)

    def __grid_buy(self, date, price):

        lower10, tolerance = False, True
        for m in self.memory:
            if price < m*(1-self.BUY_THRESHOLD):
                lower10 = True
            if m*(1-self.BUY_TOLERANCE) < price and price < m*(1+self.BUY_TOLERANCE):
                tolerance = False
        if lower10 == True and tolerance == True:
            purchaseAmount = self.portfolio['cash']*self.BUY_POWER / price
            purchasePrice = price
            if self.portfolio['cash'] > 0 and purchaseAmount > self.MIN_AMOUNT:
                self.portfolio['prod'].append([date, purchaseAmount, purchasePrice])
                self.portfolio['cash'] -= purchaseAmount * purchasePrice
                self.portfolio['value'] += purchaseAmount * purchasePrice
        pass

    def __grid_sell(self, price):
        for p in self.portfolio['prod']:
            date, purchaseAmount, purchasePrice = p
            if purchasePrice * (1+self.SELL_THRESHOLD) <= price:
                self.portfolio['cash'] += purchaseAmount*price
                self.portfolio['value'] -= purchaseAmount*purchasePrice
                self.portfolio['prod'].remove(p)
        pass


