# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_colums(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if filters:
	 	return frappe.db.sql("""select po.name,po.type,po.supplier,po.company,po.transaction_date,po.is_subcontracted,po.supplier_address,po.customer_purchase_order_no,po.grand_total,
	 							po_item.item_name,po_item.item_group,
  								po_item.description,po_item.stock_uom,
  								po_item.qty,po_item.qty,
  								po_item.rate,po_item.base_net_rate,	
  								po_item.amount,po_item.base_net_amount  
								from
									`tabPurchase Order` po,`tabPurchase Order Item` po_item
								where
									po.name = '{0}' and po_item.parent ='{1}' and (po.status ='Draft' or po.status = 'To Receive and Bill')
									""".format(filters.name,filters.name),as_list=1)
	else:
		data=[]
		# total_row = [[u'PO-00024', u'LPO', u'Onkar Mfg', u'EMI', u'', u'No', u'Onkar Mfg-Billing', u'5555', 900.0, u'Bras Handles', u'Products', u'Bras Handles', u'Kg', 3.0, 3.0, 300.0, 300.0, 900.0, 900.0]]

		total_row = [[u'', u'', u'', '','', u'', u'', u'',0.0, u'', u'', u'', u'',0.0,0.0,0.0,0.0, 0.0,0.0]]
		last_row = [[u'', u'', u'', '','', u'', u'', u'',0.0, u'', u'', u'', u'',0.0,0.0,0.0,0.0, 0.0,0.0]]

		purchase_orders = frappe.db.sql("""select po.name from `tabPurchase Order`po where po.status = 'Draft' or 
											po.status = 'To Receive and Bill' """,as_dict=1) 

		for order in purchase_orders:
			print "orders",order
			data1 = []
			data1 = frappe.db.sql("""select po.name,po.type,po.supplier,po.company,po.transaction_date,po.is_subcontracted,po.supplier_address,po.customer_purchase_order_no,po.grand_total,
	 							po_item.item_name,po_item.item_group,
  								po_item.description,po_item.stock_uom,
  								po_item.qty,po_item.qty,
  								po_item.rate,po_item.base_net_rate,	
  								po_item.amount,po_item.base_net_amount  
								from
									`tabPurchase Order` po,`tabPurchase Order Item` po_item
								where
									po.name = '{0}' and po_item.parent ='{1}' and (po.status ='Draft' or po.status = 'To Receive and Bill')
									""".format(order['name'],order['name']),as_list=1)
			print "data1",data1
			print "\n\n\_______________________"
			total_row = get_total_sales_amount(data1)
			last_row  = get_last_total(last_row,total_row)   
			data.extend(data1)
			data.extend(total_row)
		data.extend(last_row)
		return data

def get_colums(filters):
	columns =[ ("Purchase Order") + ":Link/Purchase Order:100",
				   ("Type") +":Data:70",
 				   ("Party") + ":Data:150",
				   ("Company") + " :Data:120",
				   ("Date") + ":Date:110",
				   ("Supply Raw Materials") + ":Data:120",
				   ("Address") + ":Data:140",
				   ("Purchase Order No")+ ":Data:130",
				   ("Amount") + ":Currency:140",
				   ("Item Name") + ":Data:100" ,
				   ("item_group") + ":Data:100",
				   ("Description") + ":Data:100",
				   ("UOM") + ":Data:50",
				   ("Qty") + ":Float:50" , 
				   ("Pending") + ":Float:60",
				   ("Rate") + ":Currency:120",
				   ("Net Rate") + ":Currency:120", 
		  		   ("Amount") + ":Currency:80",
		  		   ("Net Amount") + ":Currency:80" 
		  		
			]
	return columns


def get_total_sales_amount(item_list):
	amount = 0.0
	qty = 0.0
	pending_qty = 0.0
	rate = 0.0
	net_rate = 0.0
	amount1 = 0.0
	net_amount =0.0
	for item in item_list:
		amount = amount +float(item[8])
		qty = qty + float(item[13])
		pending_qty = pending_qty + float(item[14])
		rate = rate + float(item[15])
		net_rate = net_rate + float(item[16])
		amount1 =amount1 + float(item[17])
		net_amount = net_amount + float (item[18])
		
	return [[u'', u'', u'', '','', u'', u'', u'',amount, u'', u'', u'', u'',qty,pending_qty,rate,net_rate, amount1, net_amount]]

def get_last_total(last_row,item_list):
	
	amount = float(last_row[0][8])
	qty = float(last_row[0][13])
	pending_qty = float(last_row[0][14])
	rate = float(last_row[0][15])
	net_rate = float(last_row[0][16])
	amount1 = float(last_row[0][17])
	net_amount = float(last_row[0][18])


	for item in item_list:
		amount = amount +float(item[8])
		qty = qty + float(item[13])
		pending_qty = pending_qty + float(item[14])
		rate = rate + float(item[15])
		net_rate = net_rate + float(item[16])
		amount1 =amount1 + float(item[17])
		net_amount = net_amount + float (item[18])
		
	return [[u'', u'', u'', '','', u'', u'', u'',amount, u'', u'', u'', u'',qty,pending_qty,rate,net_rate, amount1, net_amount]]

