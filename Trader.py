class SellTrigger:
    def __init__(self, parameters):
        self.parameters = parameters

    def generate(self, price, portfolio):
        r = []
        for p in portfolio['prod']:
            purchaseDate, purchaseAmount, purchasePrice = p
            if purchasePrice * (1+self.parameters["SELL_THRESHOLD"]) <= price:
                r.append((p, price))
        return r


class BuyTrigger:
    def __init__(self, parameters):
        self.parameters = parameters

    def generate(self, price, leads, cash):
        r = [(0,0)]
        lower10, tolerance = False, True
        for m in leads:
            if price < m*(1-self.parameters["BUY_THRESHOLD"]):
                lower10 = True
            if m*(1-self.parameters["BUY_TOLERANCE"]) < price and price < m*(1+self.parameters["BUY_TOLERANCE"]):
                tolerance = False
        if lower10 == True and tolerance == True:
            purchaseAmount = cash*self.parameters["BUY_POWER"] / price
            purchasePrice = price
            if cash > 0 and purchaseAmount > self.parameters["MIN_AMOUNT"]:
                r = [(purchaseAmount, purchasePrice)]
        return r

class Trader:
    def __init__(self, deposite):
        self.portfolio = {'cash':deposite, 'value':0, 'prod':[]}
        # TODO get portfolio
        # self.portfolio = self.__retrive_portfolio()
        self.leads = [0]*10
        self.parameters = {
                "MIN_AMOUNT": 0.001,
                "BUY_THRESHOLD": 0.1,
                "BUY_TOLERANCE": 0.03,
                "BUY_POWER": 0.1,
                "SELL_THRESHOLD": 0.03,}
        self.buyTriggers = [BuyTrigger(self.parameters)]
        self.sellTriggers = [SellTrigger(self.parameters)]

    def query_portfolio(self,date):
        print(date, self.portfolio['cash'], self.portfolio['value'])
        for item in self.portfolio['prod']:
            #print(item)
            pass
        pass

    def trade(self, info):
        date,price = info

        for buyTrigger in self.buyTriggers:
            r = buyTrigger.generate(price,self.leads,self.portfolio['cash'])
            # TODO execute
            self.__update_on_buy(date, r)


        for sellTrigger in self.sellTriggers:
            triggers = sellTrigger.generate(price, self.portfolio)
            self.__update_on_sell(date, triggers)

        self.__update_leads(price)

        r = []
        for trigger in triggers:
            (purchase, sellPrice) = trigger
            r.append([purchase[0],purchase[2],date,price])
        return r

    def __update_on_buy(self, date, triggers):
        purchaseAmount, purchasePrice = triggers[0]
        if purchaseAmount != 0:
            self.portfolio['prod'].append([date, purchaseAmount, purchasePrice])
            self.portfolio['cash'] -= purchaseAmount * purchasePrice
            self.portfolio['value'] += purchaseAmount * purchasePrice
        pass

    def __update_on_sell(self, date, triggers):
        for trigger in triggers:
            (purchase, sellPrice) = trigger
            purchaseDate, purchaseAmount, purchasePrice = purchase
            self.portfolio['cash'] += purchaseAmount*sellPrice
            self.portfolio['value'] -= purchaseAmount*purchasePrice
            self.portfolio['prod'].remove(purchase)
        pass

    def __update_leads(self, price):
        new_record = price
        self.leads.append(new_record)
        self.leads.pop(0)


