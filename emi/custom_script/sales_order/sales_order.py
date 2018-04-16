
from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.utils import money_in_words
from frappe.utils import flt, cint, nowdate,get_datetime
from frappe.utils import cstr
from frappe import _
from bs4 import BeautifulSoup
from frappe.utils import money_in_words


@frappe.whitelist()
def get_sales_person(doctype, txt, searchfield, start, page_len, filters):
	emp=frappe.db.sql("""select name from `tabEmployee` where name=(select employee from `tabSales Person`   where name = (select  sales_person from `tabSales Team`  where parenttype = 'Customer' and parent = '%s' limit 1))"""%(filters.get('customer')))
	return emp
@frappe.whitelist()
def validate (doc,method=None):
	discount_amount = delivery_charge = 0.0

	for tax in doc.taxes:
		if doc.shipping_rule:
			shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
			if tax.account_head == shipping_rule_doc.account:
				doc.delivery_charge = tax.tax_amount
		
		if tax.account_head == "Output VAT  - E":
			printformat_vat_tax = tax.tax_amount

	doc.printformat_net_total = (doc.total - doc.discount_amount) + flt(doc.delivery_charge)
	# doc.printformat_net_total_with_tax = printformat_net_total + printformat_vat_tax
	# doc.printformat_net_total = printformat_net_total
	# doc.printformat_vat_tax = printformat_vat_tax
	# doc.printformat_in_word = money_in_words(doc.printformat_net_total_with_tax, doc.currency)


