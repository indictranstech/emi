# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JobCard(Document):

	def on_submit(self):
		self.stock_entry_through_job_cart()

	def stock_entry_through_job_cart(self):
		si = None
		for chld in self.job_order_detail:
			if chld.process == "Final Inspection":
				po = frappe.db.sql("""select * from `tabProduction Order` where name ='{0}'""".format(chld.production_order),as_dict=1)
				print po, po[0]['fg_warehouse'], "uhhsdfdsb"
				# po = frappe.db.sql("""select name, company, fg_warehouse, production_item,stock_uom  from `tabProduction Order` where name = {}""".format(chld.production_order))
				 # = "PRO-00007"
				si = frappe.get_doc({
					"doctype": "Stock Entry",
					"purpose": "Material Transfer",
					"posting_date": chld.date,
					"from_warehouse": po[0]['fg_warehouse'],
					"to_warehouse": "Final Inspected Warehouse - E",
					"items": get_order_items(po, chld, po[0]['fg_warehouse'], "Final Inspected Warehouse - E")
				})
		si.flags.ignore_mandatory = True
		si.save(ignore_permissions=True)
		si.submit()
		frappe.db.commit()		


def get_order_items(po, chld, s_warehouse, t_warehouse):
	 	items = []
	 	items.append({
			"s_warehouse": s_warehouse,
			"t_warehouse": t_warehouse,
			"item_code": po[0]['production_item'],
			"qty": float(chld.completed_job),
			"uom": po[0]['stock_uom'],
		})
		return items		

@frappe.whitelist()
def get_info_production(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabProduction Order` where status='In Process'""",as_list=1,debug=1)
