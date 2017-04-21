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
	 	return frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,
	 							so.po_no,so.grand_total,so_item.item_name,so_item.item_group,
  								so_item.description,so_item.stock_uom,
  								so_item.qty,so_item.qty,
  								so_item.rate,so_item.base_net_rate,	
  								so_item.amount,so_item.base_net_amount  
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									so.name = '{0}' and so_item.parent ='{1}' and (so.status ='Draft' or so.status = 'To Deliver and Bill')
								order by so.name desc""".format(filters.name,filters.name),as_list=1)
	else:
		return frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,so.po_no,
				so.grand_total from `tabSales Order` so where so.status = 'Draft' or 
				so.status = 'To Deliver and Bill'""",as_list=1) 


def get_colums(filters):
	columns =[ ("Sales Order") + ":Link/Sales Order:100",
				   ("Party") + ":Data:150",
				   ("Company") + ":Data:120",
				   ("Date") + ":Date:100",
				   ("Delivery Date") + ":Date:100",
				   ("Contact Person")+ " :Data:140",
				   ("Address")+":Data:180",
				   ("Ref No") + ":Data:140",
				   ("Amount") + ":Currency:120"

				 ]
	if filters:
		columns.extend( [
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
				  	)
	return columns
