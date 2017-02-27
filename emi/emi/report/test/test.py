# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	return columns, data
	columns, data = [], []
	columns = get_colums()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if filters:
		return frappe.db.sql("""
						select production_order,date from `tabJob Order`""",as_list=1)
			# case when 1=1 
			# 	then (select IFNULL(sum(mr.job_allocated),"0.0")
			# 	from `tabJob_Order_Detail` 	
	else:
		return []	


def get_colums():
	columns = [("Production Order") + ":Data:150"] + \
			  [("Client") + ":Link/Customer:100"] + \
			  [("Phone") + ":Data:100"] + \
			  [("Sales Invoice") + ":Link/Sales Invoice:100"] + \
			  [("Order Summary") + ":Data:500"] + \
			  [("Balance") + ":Currency:120"] + \
			  [("Cash Dollars") + ":Float:120"] + [("Cash Gourdes") + ":Currency:120"] + \
			  [("Cheque Dollars") + ":Float:120"] + [("Cheque Gourdes") + ":Currency:120"] + \
			  [("Credit Card") + ":Currency:80"] + \
			  [("Carte/Credit") + ":Currency:120"] + \
			  [("Total Payments") + ":Currency:120"] +\
			  [("Invoice Total") + ":Currency:120"]
	return columns	


	
