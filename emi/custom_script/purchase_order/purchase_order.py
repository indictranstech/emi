from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr,get_datetime
from frappe import _

@frappe.whitelist()
def validate(self,method=None):
	for row in self.items:
		if len(self.items) > 6:
			if float(row.idx) % 6 == 0:
				row.page_break = 1
