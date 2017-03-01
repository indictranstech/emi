# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VendorEvaluation(Document):
	pass
# @frappe.whitelist()
# def make_vendor_evaluation(source_name, target_doc=None):
# 	doc = get_mapped_doc("Supplier", source_name, {
# 		"Supplier": {
# 			"doctype": "Vendor Evaluation",
# 			"field_map": {
# 				"website": "website",
# 				"branch": "branch",
# 				"nature_of_business": "nature_of_business",
# 				"bank_account_no":"bank_account_no",
# 				"account_name":"account_name"
# 			},
# 		}
# 	},target_doc, postprocess)

# 	return doc