
from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.utils import money_in_words


@frappe.whitelist()
def get_sales_person(doctype, txt, searchfield, start, page_len, filters):
	emp=frappe.db.sql("""select name from `tabEmployee` where name=(select employee from `tabSales Person`   where name = (select  sales_person from `tabSales Team`  where parenttype = 'Customer' and parent = '%s' limit 1))"""%(filters.get('customer')))
	return emp
@frappe.whitelist()
def validate (doc,method=None):

	printformat_net_total = printformat_vat_tax = 0.0
	discount_amount = delivery_charge = 0.0
	for tax in doc.taxes:
		if tax.account_head == "Stock Adjustment - E":
			delivery_charge = tax.tax_amount

	if doc.discount_amount:
		discount_amount = doc.discount_amount
		
	doc.delivery_charge = delivery_charge
	printformat_net_total = (doc.total - discount_amount) + delivery_charge
	printformat_vat_tax = (printformat_net_total * 5)/100
	doc.printformat_net_total_with_tax = printformat_net_total + printformat_vat_tax
	doc.printformat_net_total = printformat_net_total
	doc.printformat_vat_tax = printformat_vat_tax
	doc.printformat_in_word = money_in_words(doc.printformat_net_total_with_tax, doc.currency)


