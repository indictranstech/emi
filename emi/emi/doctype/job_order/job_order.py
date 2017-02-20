# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JobOrder(Document):
	pass
# def get_sub_contract_entry(doc, method):
# 	bom_no = frappe.db.get_value("BOM", doc.bom_no, "item_name")
# 		for i in doc.items:
# 			qty = i.qty
# 		se.append("items", {
# 		"item_code": bom_no,
# 		"quantity": qty
# 		})
@frappe.whitelist()
def get_info_production(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabProduction Order` where status='In Process'""",as_list=1,debug=1)
