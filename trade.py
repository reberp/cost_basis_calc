#for the class 
from enum import Enum 


def lower_amt_obj(buy,sell):
	return sell if sell.amt<=buy.amt else buy
	#return higher_amt(sell,buy) #why the absolute fuck doesn't this work

def higher_amt_obj(buy,sell):
	return sell if buy.amt<sell.amt else buy


class Trade:
	
	def __init__(self,list):
		self.date = list[0]
		self.type = list[1]	
		self.amt  = list[2]
		self.price_per = list[3]

	def to_list(self):
		#print("{}".format([self.date,self.type,self.amt,self.price_per]))
		return [self.date,self.type,self.amt,self.price_per]

	def __repr__(self):
		return repr("{}: {} {} at {} per".format(self.date, self.type, round(self.amt,8), self.price_per))


class F8949_Trade(Trade):

	def __init__(self,amt,bought_date,bought_at,sold_date,sold_at,asset="test"):
		self.amt = amt
		self.bought_date = bought_date
		self.bought_at = bought_at
		self.sold_date = sold_date
		self.sold_at = sold_at
		self.profit = (sold_at*amt) - (bought_at*amt)
		self.asset=asset
		#print("{}: Bought {} @ {} per. {}: Sold @ {} per".format(self.bought_date,round(self.amt,8),self.bought_at,self.sold_date,self.sold_at))

	def __repr__(self):
		return repr("{}: Bought {} @ {} per. {}: Sold @ {} per".format(self.bought_date,round(self.amt,8),self.bought_at,self.sold_date,self.sold_at))



