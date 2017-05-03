# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_colums(filters)
	data = get_data(filters)
	return columns, data
def get_sales_orders(filters):
	if filters:
		return frappe.get_all("Sales Order",fields=["name"], filters = {})
	else:
		return frappe.get_all("Sales Order",fields=["name"])


def get_data(filters):
	
	if filters:
		cond = "";
		last_row = [['','', '', '', 0.0, 0.0,0.0,'',0.0]]
		filter_data = [];
		sr = 0;
		# --------- By  Sales Oder-------------
		if filters.name:
			cond = "so.name = '{0}' and so_item.parent = '{1}'".format(filters.name,filters.name)
			filter_data =frappe.db.sql("""select so.name,so.customer,so_item.item_name,so_item.item_group,
  								so_item.qty,so_item.base_net_amount,so_item.amount 
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									{0} 
								order by so.name desc""".format(cond),as_list=1)
	 	
	 		
	 		sales_return = get_sales_return(filters.name)
		 	if sales_return:
		 		sr = float(sales_return[0][0])
		 	for data in filter_data:
	 			data.append(sr)
	 			val = float(data[6] - (-1*(data[7])))
	 			data.append(val)
	 		total_row = get_total_sales_amount(filter_data)
	 		if total_row:
	 			last_row= get_last_total(last_row,total_row)
	 			# filter_data.extend(total_row)
		else:
			
			#----By Filters Customer and Date_________
			fltr={}
			sales_oders = '' 
			if filters.customer and filters.from_date and filters.to_date:
				cond = "so_item.parent = so.name and so.customer ='{0}' and so.transaction_date between '{1}' and '{2}'".format(filters.customer,filters.from_date,filters.to_date)				
				sales_oders = frappe.db.sql("""select so.name from `tabSales Order` so,`tabSales Order Item` so_item
												where
												{0}	 
												order by so.name desc""".format(cond),as_dict=1)

			else:
				if filters.from_date and filters.to_date:
					cond = "so_item.parent = so.name and so.transaction_date between '{0}' and '{1}'".format(filters.from_date,filters.to_date)
					# fltr.update({['Sales Order','transaction_date','between',filters.from_date,'and',filters.to_date]})
					sales_oders = frappe.db.sql("""select so.name from `tabSales Order` so ,`tabSales Order Item` so_item
												where
												{0}	 
												order by so.name desc""".format(cond),as_dict=1)
					
				else:
					if filters.customer:
						fltr.update({"customer":filters.customer})
						sales_oders = get_sales_orders(fltr)
						
						customer_sales_oders = get_sales_orders(fltr)
						cond = "so_item.parent = so.name and so.customer ='{0}'".format(filters.customer)
			
			for order in sales_oders:
				cond = "so.name = '{0}' and so_item.parent = '{1}'".format(order['name'],order['name'])
				order_wise_data =  frappe.db.sql("""select so.name,so.customer,so_item.item_name,so_item.item_group,
  													so_item.qty,so_item.base_net_amount,so_item.amount 
													from
														`tabSales Order` so,`tabSales Order Item` so_item
													where
														{0}									 
													order by so.name desc""".format(cond),as_list=1)
				if order_wise_data:
					sales_return = get_sales_return(order['name'])
				if sales_return:
					sr = float(sales_return[0][0])
				for data in order_wise_data:
		 			data.append(sr)
		 			val = float(data[6] - (-1*(data[7])))
		 			data.append(val)
				total_row = get_total_sales_amount(order_wise_data)
				if total_row:
		 			last_row= get_last_total(last_row,total_row)
		 			order_wise_data.extend(total_row)
				filter_data.extend(order_wise_data)
							 	
		filter_data.extend(last_row)					
	 	return filter_data
	else:
		#-------Without Any Filter
		sales_oders= get_sales_orders(filters)
		data = []
		total_row = [['', '','', '','','', '']]
		last_row = [['','', '', '', 0.0, 0.0,0.0,'',0.0]]
		if sales_oders:
			for order in sales_oders:
				data1 = frappe.db.sql("""select so.name,so.customer,so_item.item_name,so_item.item_group,
  								so_item.qty,so_item.base_net_amount,so_item.amount 
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									so.name = '{0}' and so_item.parent ='{1}' 
								order by so.name desc""".format(order['name'],order['name']),as_list=1)
				if data1:
					sr=0
					sales_return = frappe.db.sql(""" select dn.grand_total from `tabDelivery Note` dn,
													`tabDelivery Note Item` dn_item where 
													 dn_item.parent = dn.name and dn.is_return=1 
													 and  dn_item.against_sales_order ='{0}'""".format(order['name']))
					
					if sales_return:
						sr  = float(sales_return[0][0])

					for s in range(0,len(data1)):
						data1[s].append(sr)
						val=float(data1[s][6] - (-1*(data1[s][7])))
						data1[s].append(val)
					
					data.extend(data1)
					total_row = get_total_sales_amount(data1)
					last_row= get_last_total(last_row,total_row)
					data.extend(total_row)
		
		data.extend(last_row)			
		return data


def get_colums(filters):
	columns =[ ("Sales Order") + ":Link/Sales Order:100",
				   ("Party") + ":230",
				   ("Item Name") + ":Data:100",
				   ("Item Group") + ":Data:100",
				   ("Qty") + ":Float:60" ,
				   ("Amount") + ":Currency:120",
				   ("Net Sales") + ":Currency:120",
				   ("Sales Return") + ":Data:120",
				   ("Sales Amount") +":Data:120"
			]
	return columns


def get_total_sales_amount(item_list):
	net_sale = 0
	qty = 0
	sales_amount = 0
	for item in item_list:
		qty = qty + float(item[4])
		net_sale = net_sale+float (item[5])
		sales_amount= sales_amount + float (item[6])
		val = float(item[8])
	return [['','','','',qty,net_sale,sales_amount,'',val]]

def get_last_total(last_row,total_row):
	net_sale = float(last_row[0][5])
	qty = float(last_row[0][4])
	sales_amount = float(last_row[0][6])
	val = float(last_row[0][8])
	
	for row in total_row:
		qty = qty + float(row[4])
		net_sale = net_sale + float(row[5])
		sales_amount = sales_amount + float(row[6])
		val = val +float(row[8])
	return [['','','','',qty,net_sale,sales_amount,'',val]]

# def get_final_amount(row):




def get_sales_return(sales_oders):
	return frappe.db.sql(""" select dn.grand_total from `tabDelivery Note` dn,
						`tabDelivery Note Item` dn_item where 
						dn_item.parent = dn.name and dn.is_return=1 
						and  dn_item.against_sales_order ='{0}'""".format(sales_oders))
