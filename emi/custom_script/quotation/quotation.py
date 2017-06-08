
from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _



@frappe.whitelist()
def get_sales_person(doctype, txt, searchfield, start, page_len, filters):
	emp=frappe.db.sql("""select name from `tabEmployee` where name=(select employee from `tabSales Person`   where name = (select  sales_person from `tabSales Team`  where parenttype = 'Customer' and parent = '%s' limit 1))"""%(filters.get('customer')))
	return emp
	