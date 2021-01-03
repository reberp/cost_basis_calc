#!/usr/bin/env python3

"""

csv format:
date,action,amount,price_per
2020,buy,1,100
2020,buy,1,200
2020,sell,1,500


"""

import argparse
import datetime
import trade 
import tools_8949


def load_contents(filename):
	#could probaly just do it all inline as its read but w/e
	fh = open(filename,'r')
	header=fh.readline()
	trades = fh.readlines()
	for line in trades:
		line = line.rstrip().split(',')
		line[2]=float(line[2])
		line[3]=float(line[3])
		buys.append(line) if 'buy' in line else sells.append(line)

def process_trades(year):
	#take oldest buy -> match to first sale, del and repeat 
	# if sale is more, update sale amount, create new sale and calculate profit
	# if buy is more, update buy amount, create new buy and calculate profit
	total_profit  	= 0
	yearly_profit 	= 0
	while (buys!=[] and sells !=[]):
		sell= trade.Trade(sells.pop(0))
		buy = trade.Trade(buys.pop(0))

		traded_amt 		= trade.lower_amt_obj(buy,sell).amt
		higher_amt_obj 	= trade.higher_amt_obj(buy,sell)

		sale_amt 		= traded_amt * sell.price_per
		cost_basis_amt 	= traded_amt * buy.price_per

		higher_amt_obj.amt = higher_amt_obj.amt-traded_amt 						#set leftover
		buy_sell_dict[higher_amt_obj.type].insert(0,higher_amt_obj.to_list()) 	#carry leftover to next trade		

		profit 			= sale_amt - cost_basis_amt
		total_profit	= profit+total_profit
		#print("{},buy,{:.8f},{:.2f}\n{},sell,{:.8f},{:.2f}\t{}".format(buy.date,round(traded_amt,8),buy.price_per,sell.date,round(traded_amt,8),sell.price_per,profit))
		
		bought_date = datetime.date.fromisoformat(buy.date[0:10])
		sold_date 	= datetime.date.fromisoformat(sell.date[0:10])
		term 		= "short" if (sold_date-bought_date).days<365 else "long"

		if sold_date.year == year:
			yearly_profit += profit
			trade_term_dict[term].append(trade.F8949_Trade(traded_amt,str(bought_date),buy.price_per,str(sold_date),sell.price_per))


if __name__ == "__main__":

	modes=['fifo','lifo']
	buys = [] 
	sells= []
	short_8949 = []
	long_8949 = []
	buy_sell_dict = {'buy':buys,'sell':sells}
	trade_term_dict =  {'short':short_8949,'long':long_8949}

	parser = argparse.ArgumentParser(description='hello')
	parser.add_argument('-f', help="csv of trades", type=str, required=False, default="test.csv")
	parser.add_argument('-m', help="mode", type=str, required=False, choices=modes, default='fifo')
	parser.add_argument('-y', help="year to calculate", type=int, required=False, default=2020)
	parser.add_argument('-t', help="name of blank 8949", type=str, required=False, default="f8949.pdf")
	parser.add_argument('-o', help="output 8949 filename", type=str, required=False, default='output8949.pdf')
	args = parser.parse_args()

	load_contents(args.f)
	process_trades(args.y)

	tools_8949.write_8949(trade_term_dict,args)
