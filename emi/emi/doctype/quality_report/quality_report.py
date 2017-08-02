# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class QualityReport(Document):
	pass
@frappe.whitelist()
def get_so_items(source_name, target_doc=None):
	doc = get_mapped_doc("Sales Order", source_name,	{
		"Sales Order": {
			"doctype": "Quality Report",
			"customer":"customer"
		},
		"Sales Order Item": {
			"doctype": "Quality Items",
			"field_map": {
				"item_code": "item",
				"warehouse": "warehouse",
			},
		}
	},target_doc)
	return doc