# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class JobCard(Document):

	def on_submit(self):
		self.check_pro_order()

	def validate(self):
		self.final_inspected_qty()
		

	# Create Stock Entry For Final Inspection 
	def stock_entry_through_job_cart(self):
		# Stock Entry For Final Inspected Qty
		for chld in self.job_order_detail:
			if chld.process == "Final Inspection":
				po = frappe.get_doc("Production Order", chld.production_order)
				si = frappe.get_doc({
					"doctype": "Stock Entry",
					"purpose": "Material Transfer",
					"posting_date": chld.date,
					"from_warehouse": po.get('fg_warehouse'),
					"to_warehouse": "Stores - E",
					"items": get_order_items(po, chld, po.get('fg_warehouse'), "Stores - E")
				})
				si.flags.ignore_mandatory = True
				si.save(ignore_permissions=True)
				si.submit()
				frappe.db.commit()

#To Check Quantity is not Greater Than Production Order Quantity
	def final_inspected_qty(self):
		for chld in self.job_order_detail:
			if chld.process == 'Final Inspection'  and  flt(self.quantity)<flt(chld.completed_job):
				frappe.throw("You Have Not Allowed to entered the Greater Value from Production Order Quantity")

	def check_pro_order(self):
		po_status= frappe.db.get_value("Production Order",{"name":self.production_order},"status")
		if po_status =='In Process':
			frappe.throw("Please First Submit The Production Order")
		else:
			self.stock_entry_through_job_cart()

def get_order_items(po, chld, s_warehouse, t_warehouse):
	 	# Items from Production Order
	 	items = []
	 	items.append({
			"s_warehouse": s_warehouse,
			"t_warehouse": t_warehouse,
			"item_code": po.get('production_item'),
			"qty": float(chld.completed_job),
			"uom": po.get('stock_uom'),
		})
		return items		


@frappe.whitelist()
def get_info_production(doctype, txt, searchfield, start, page_len, filters):
	#Production Order Process Filter in Job Card
	return frappe.db.sql("""select name from `tabProduction Order` where status='In Process'""",as_list=1,debug=1)

"""
get_query for Pending Sales order report
"""
@frappe.whitelist()
def sales_order_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabSales Order`
		where status = 'Draft' or status = 'To Deliver and Bill' """,as_list=1)

"""
get_query for Pending Purchase order report
"""
@frappe.whitelist()
def purchase_order_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select po.name,po.transaction_date,po.supplier
							from `tabPurchase Order` po where po.status = 'Draft' or 
							po.status = 'To Receive and Bill' """,as_list=1)
"""
get_query for item shortest report for raw material
"""

@frappe.whitelist()
def product_query(doctype, txt, searchfield, start, page_len, filters):
       return frappe.db.sql(" select bin.item_code from tabBin bin,tabItem i where bin.projected_qty <0 and i.item_code =bin.item_code and i.item_group ='Products'",as_list=1)



