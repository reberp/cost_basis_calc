
""">>> from fdfgen import forge_fdf
>>> fields = [('topmostSubform[0].Page2[0].f2_118[0]','hello'),('topmostSubform[0].Page2[0].Table_Line1[0].Row14[0].f2_109[0]','hello2')]
>>> fdf = forge_fdf("",fields,[],[],[])
>>> with open("data.fdf","wb") as fdf_file:
...     fdf_file.write(fdf)

"""
#pdftk f8949.pdf fill_form data.fdf output output.pdf flatten

"""
Selection boxes (gets 1,2,3 respectively to check):
FieldName: topmostSubform[0].Page1[0].c1_1[0]
FieldName: topmostSubform[0].Page1[0].c1_1[1]
FieldName: topmostSubform[0].Page1[0].c1_1[2] -> 3
...
FieldName: topmostSubform[ls0].Page2[0].c2_1[2] -> 3


text fields (line 1-14) (gets text values to input) (page 1 is short-term)
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_3[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_4[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_5[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_6[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_7[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_8[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_9[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row1[0].f1_10[0]
FieldName: topmostSubform[0].Page1[0].Table_Line1[0].Row2[0].f1_11[0]
...
FieldName: topmostSubform[0].Page2[0].Table_Line1[0].Row1[0].f2_3[0]

"""

"""
F8949_trade
		self.amt = amt
		self.bought_date = bought_date
		self.bought_at = bought_at
		self.sold_date = sold_date
		self.sold_at = sold_at
		self.profit = (sold_at*amt) - (bought_at*amt)
"""

from fdfgen import forge_fdf
from math import ceil
import trade
from os import system

def write_to_binary(docfields,num):
	fdf = forge_fdf("",docfields,[],[],[])
	with open("doc_{}.fdf".format(num),'wb') as fdf_file:
		fdf_file.write(fdf)

def combine_into_doc(args,num):
	cmd_string = """pdftk {} fill_form "doc_{}.fdf" output "doc_{}.pdf" flatten""".format(args.t,num,num)
	system(cmd_string)

def write_row(docfields,trade,page,i,row_num):
	docfields.append(('topmostSubform[0].Page{}[0].Table_Line1[0].Row{}[0].f{}_{}[0]'.format(page,row_num,page,i*8+3),"{} {}".format(round(trade.amt,8), trade.asset )))
	docfields.append(('topmostSubform[0].Page{}[0].Table_Line1[0].Row{}[0].f{}_{}[0]'.format(page,row_num,page,i*8+4),"{}".format(trade.bought_date)))
	docfields.append(('topmostSubform[0].Page{}[0].Table_Line1[0].Row{}[0].f{}_{}[0]'.format(page,row_num,page,i*8+5),"{}".format(trade.sold_date)))
	docfields.append(('topmostSubform[0].Page{}[0].Table_Line1[0].Row{}[0].f{}_{}[0]'.format(page,row_num,page,i*8+6),"{}".format(round(trade.sold_at*trade.amt,2))))
	docfields.append(('topmostSubform[0].Page{}[0].Table_Line1[0].Row{}[0].f{}_{}[0]'.format(page,row_num,page,i*8+7),"{}".format(round(trade.bought_at*trade.amt,2))))
	docfields.append(('topmostSubform[0].Page{}[0].Table_Line1[0].Row{}[0].f{}_{}[0]'.format(page,row_num,page,i*8+10),"{}".format(round(trade.profit,2))))

def write_final_row(docfields,page,total_cost,total_proceeds):
	docfields.append(('topmostSubform[ls0].Page{}[0].c{}_1[2]'.format(page,page),3)) #actually the first row but w/e 			
	total_profit = round(total_proceeds - total_cost,8)
	docfields.append(('topmostSubform[0].Page{}[0].f{}_115[0]'.format(page,page),round(total_proceeds,2)))
	docfields.append(('topmostSubform[0].Page{}[0].f{}_116[0]'.format(page,page),round(total_cost,2)))
	docfields.append(('topmostSubform[0].Page{}[0].f{}_119[0]'.format(page,page),round(total_profit,2)))

def write_page(page,docfields,trades):
	total_proceeds = 0 
	total_cost = 0 
	for i in range(len(trades)):
		row_num=i+1
		trade = trades[i]
		write_row(docfields,trade,page,i,row_num)		
		total_proceeds += trade.sold_at*trade.amt
		total_cost += trade.bought_at*trade.amt	
	write_final_row(docfields,page,total_cost,total_proceeds)	

def write_8949(trade_term_dict,args): 
	# |-> factory? 
	
	#fields=[] #[[(doc1val1,doc1val2)][doc2...]]
	num_short_pages = ceil(len(trade_term_dict['short'])/14)
	num_long_pages = ceil(len(trade_term_dict['long'])/14)

	for doc_num in range(max(num_short_pages,num_long_pages)):

		docfields=[]
		add_to_doc=[]
		trade_range_start = doc_num*14
		if trade_term_dict['short'][trade_range_start:trade_range_start+14]:
			add_to_doc.append(1)
		if trade_term_dict['long'][trade_range_start:trade_range_start+14]:
			add_to_doc.append(2)
		for page in add_to_doc:
			cur_page_trades = trade_term_dict[{1:'short',2:'long'}[page]]
			write_page(page,docfields,cur_page_trades)


		write_to_binary(docfields,doc_num)
		combine_into_doc(args,doc_num)

