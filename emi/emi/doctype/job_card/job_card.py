# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JobCard(Document):
	pass
@frappe.whitelist()
def get_info_production(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabProduction Order` where status='In Process'""",as_list=1,debug=1)
