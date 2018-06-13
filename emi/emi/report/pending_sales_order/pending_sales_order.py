# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cint, nowdate,get_datetime
from erpnext.accounts.utils import get_currency_precision

def execute(filters=None):
	columns, data = [], []
	columns = get_colums(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):

	precision = int(frappe.db.get_value("System Settings",{"name":"System Settings"},"float_precision"))
	# currency_precision = get_currency_precision() or 3
	data=[]

	if filters:
		project_row = [['Remark', '', '', '','', '', '', '','', '', '', '', '','','','','', '','','']]
		total_row = [['Sub Total', '', '', '','', '', '', '',0.0, '', '', '', '',0.0,0.0,0.0,0.0, 0.0,0.0,0.0]]
		last_row = [['', '', '', '','', '', '', '',0.0, '', '', '', '',0.0,0.0,0.0,0.0, 0.0,0.0,0.0]]

	 	data = []
	 	if filters.name:
	 		data1= frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,
	 							so.po_no,so.grand_total,so_item.item_name,so_item.item_group,
  								so_item.description,so_item.stock_uom,
  								so_item.qty,so_item.delivered_qty,
  								format((so_item.qty - so_item.delivered_qty),3),
  								format(so_item.rate,3),format(so_item.base_net_rate,3),	
  								format(so_item.amount,3),format(((so_item.qty - so_item.delivered_qty)*so_item.rate),2)  
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									so.name = '{0}' and so_item.parent ='{1}' and (so.status ='Draft' or so.status = 'To Deliver and Bill')
								order by so.name desc""".format(filters.name,filters.name,int(precision)),as_list=1)
	 		project_row= get_project_row(filters)
			data.extend(project_row)
			data.extend(data1)
			total_row = get_total_sales_amount(data1)
			last_row  = get_last_total(last_row,total_row) 
			data.extend(last_row)
			return data
	 	else:
	 		data=[]
			project_row = [['Remark', '', '', '','', '', '', '','', '', '', '', '','','','','', '','','']]
			total_row = [['Sub Total', '', '', '','', '', '', '',0.0, '', '', '', '',0.0,0.0,0.0,0.0, 0.0,0.0,0.0]]
			last_row = [['', '', '', '','', '', '', '',0.0, '', '', '', '',0.0,0.0,0.0,0.0, 0.0,0.0,0.0]]
			sales_orders = frappe.db.sql("select so.name,so.customer from `tabSales Order` so where so.customer = '{0}' and (so.status = 'Draft' or so.status = 'To Deliver and Bill') """.format(filters.customer),as_dict=1)
			for order in sales_orders:
				data1 = []
				data1 = frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,
	 								so.po_no,so.grand_total,so_item.item_name,so_item.item_group,
  									so_item.description,so_item.stock_uom,
  									so_item.qty,so_item.delivered_qty,
  									format((so_item.qty - so_item.delivered_qty),2),
  									so_item.rate,format((so_item.base_net_rate),2),	
  									format((so_item.amount),2),format(((so_item.qty - so_item.delivered_qty)*so_item.rate),2) 
									from
										`tabSales Order` so,`tabSales Order Item` so_item
									where
										so.name = '{0}' and so_item.parent ='{1}' and (so.status ='Draft' or so.status = 'To Deliver and Bill')
									order by so.name desc""".format(order['name'],order['name']),as_list=1)
				project_row= get_project_row(order)
				data.extend(project_row)
				data.extend(data1)
				total_row = get_total_sales_amount(data1)
				last_row  = get_last_total(last_row,total_row)   
				data.extend(total_row)
		data.extend(last_row)
		return data

	else:
		data=[]
		project_row = [['Remark', '', '', '','', '', '', '','', '', '', '', '','','','','', '','','']]
		total_row = [['Sub Total', '', '', '','', '', '', '',0.0, '', '', '', '',0.0,0.0,0.0,0.0, 0.0,0.0,0.0]]
		last_row = [['', '', '', '','', '', '', '',0.0, '', '', '', '',0.0,0.0,0.0,0.0, 0.0,0.0,0.0]]
		sales_orders = frappe.db.sql("select so.name from `tabSales Order` so where so.status = 'Draft' or so.status = 'To Deliver and Bill'""",as_dict=1)
		for order in sales_orders:
			data1 = []
			data1 = frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,
	 							so.po_no,so.grand_total,so_item.item_name,so_item.item_group,
  								so_item.description,so_item.stock_uom,
  								so_item.qty,so_item.delivered_qty,
  								format((so_item.qty - so_item.delivered_qty),2),
  								so_item.rate,format((so_item.base_net_rate),2),	
  								format((so_item.amount),2),format(((so_item.qty - so_item.delivered_qty)*so_item.rate),2)  
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									so.name = '{0}' and so_item.parent ='{1}' and (so.status ='Draft' or so.status = 'To Deliver and Bill')
								order by so.name desc""".format(order['name'],order['name']),as_list=1)
			
			project_row= get_project_row(order)
			data.extend(project_row)
			data.extend(data1)
			total_row = get_total_sales_amount(data1)
			last_row  = get_last_total(last_row,total_row)   
			data.extend(total_row)
		data.extend(last_row)
		return data
		
def get_colums(filters):
	columns =[ ("Sales Order") + ":Link/Sales Order:70",
				   ("Party") + ":Data:70",
				   ("Company") + ":Data:70",
				   ("Date") + ":Date:90",
				   ("Delivery Date") + ":Date:100",
				   ("Contact Person")+ " :Data:140",
				   ("Address")+":Data:180",
				   ("Customer PO NO") + ":Data:70",
				   ("Amount") + ":Currency:200",
				   ("Item Name") + ":Data:70" ,
				   ("Item Group") + ":Data:70",
				   ("Description") + ":Data:100",
				   ("UOM") + ":Data:50",
				   ("Qty") + ":Float:50" , 
				   ("Delivered Qty") +":Float:50",
				   ("Pending Qty") + ":Float:50",
				   ("Rate") + ":Currency:100",
				   ("Net Rate") + ":Currency:110", 
		  		   ("Amount") + ":Currency:110",
		  		   ("Net Amount") + ":Currency:180" 
			 ]
				  	
	return columns

def get_total_sales_amount(item_list):
	currency_precision = get_currency_precision() or 3
	amount = 0.0
	qty = 0.0
	pending_qty = 0.0
	rate = 0.0
	net_rate = 0.0
	amount1 = 0.0
	net_amount =0.0
	base_net_amount = 0.0
	for item in item_list:
		# print "\nitem",item
		amount = amount +flt(item[8])
		qty = qty + flt(item[13])
		pending_qty = pending_qty + flt(item[14])
		rate = rate + flt(item[15])
		# net_rate = net_rate + flt(item[16])
		amount1 =amount1 + flt(item[17])
		net_amount = net_amount + flt (item[18])
		base_net_amount = base_net_amount + flt (item[19])
	
	return [['Sub Total','', '', '','', '', '', '',flt(amount,currency_precision), '', '', '', '',qty,pending_qty,rate,'', flt(amount1,currency_precision), flt(net_amount,currency_precision),flt(base_net_amount,currency_precision)]]
	
def get_last_total(last_row,item_list):
	currency_precision = get_currency_precision() or 3
	amount = flt(last_row[0][8])
	qty = flt(last_row[0][13])
	pending_qty = flt(last_row[0][14])
	rate = flt(last_row[0][15])
	# net_rate = flt(last_row[0][16])
	amount1 = flt(last_row[0][17])
	net_amount = flt(last_row[0][18])
	base_net_amount = flt(last_row[0][19])

	for item in item_list:
		amount = amount +flt(item[8])
		qty = qty + flt(item[13])
		pending_qty = pending_qty + flt(item[14])
		rate = rate + flt(item[15])
		# net_rate = net_rate + flt(item[16])
		amount1 =amount1 + flt(item[17])
		net_amount = net_amount + flt(item[18])
		base_net_amount = base_net_amount + flt(item[19])
	
	return [['Grand Total', '', '', '','', '', '', '',amount,'', '', '', '',qty,pending_qty,rate,'', amount1, net_amount,base_net_amount]]

def get_project_row(order):
	if order.name:
		project = frappe.db.sql("""select project from `tabSales Order` so
						where
						so.name = '{0}' """.format(order['name']),as_list=1)
	
	if project:
		project_row = [['PROJECT :' , project[0][0], '', '','', '', '', '','', '', '', '', '','','','','', '','','']]
		return project_row

