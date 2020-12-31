#!/usr/bin/env python3

"""

csv format:
date,action,amount,price_per
2020,buy,1,100
2020,buy,1,200
2020,sell,1,500


"""

import argparse
modes=['fifo','lifo']
buys = [] 
sells= []
mapping = {'buy':buys,'sell':sells}

def load_contents(filename):
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
	total_profit=0

	while (buys!=[] and sells !=[]):
		sell= sells.pop(0) #need to just make these classes and all of this math somewhere else. 
		buy = buys.pop(0)

		sold_more = True if sell[2]>=buy[2] else False
		higher_amt = sell if sold_more else buy
		lower_amt = buy if sold_more else sell
		altering = mapping[higher_amt[1]]

		tmp = higher_amt[2]
		higher_amt[2]=lower_amt[2]
		profit = (sell[2]*sell[3]) - (buy[2]*buy[3])
		higher_amt[2]=tmp-higher_amt[2]
		altering.insert(0,higher_amt)

		total_profit=profit+total_profit

	print(total_profit)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='hello')
	parser.add_argument('-f',type=str, required=False, default="test.csv")
	parser.add_argument('-m',type=str, required=False, choices=modes, default='fifo')
	parser.add_argument('-y',type=int, required=False, default=2020)
	args = parser.parse_args()
	load_contents(args.f)
	process_trades(args.y)