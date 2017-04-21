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
		return frappe.db.sql("""select po.name,po.type,po.supplier,po.company,po.transaction_date,po.is_subcontracted,po.supplier_address,po.customer_purchase_order_no,po.grand_total
				from `tabPurchase Order` po where po.status = 'Draft' or 
				po.status = 'To Receive and Bill' """,as_list=1) 


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
