from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import flt, cint, nowdate,get_datetime
from frappe.utils import cstr
from frappe import _
from bs4 import BeautifulSoup
from frappe.utils import money_in_words

@frappe.whitelist()
def validate(doc,method=None):
	discount_amount = delivery_charge = other_amount =0.0
	
	if doc.shipping_rule:
		shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
	''' Get Shipping Charges,VAT '''
	doc.printformat_vat_tax = None
	for tax in doc.taxes:
		# if doc.shipping_rule:
		# 	shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
		# 	if tax.account_head == shipping_rule_doc.account:
		# 		doc.delivery_charge = tax.tax_amount
		# 		tax.print_flag = 0

		if tax.account_head == "Output VAT  - E":
			doc.printformat_vat_tax = tax.tax_amount
			tax.print_flag = 0

		if doc.discount_amount:
			discount_amount = doc.discount_amount

	for tax in doc.taxes:
		if tax.print_flag ==1:
			other_amount = other_amount + tax.tax_amount
	doc.printformat_other_total = other_amount
	doc.printformat_net_total = (doc.total - doc.discount_amount) + flt(doc.printformat_other_total)


def SI_submit_notification(doc,method=None):
	if doc.docstatus == 1:
		pass
		# try:
		# 	frappe.sendmail(
		# 	recipients=["sridhar@emiuae.ae","mathur@emiuae.ae"],
		# 	#recipients=["onkar.m@indictranstech.com"],
		# 	expose_recipients="header",
		# 	# sender=frappe.session.user,
		# 	# reply_to=None,
		# 	subject="Sales Invoice Submit Notifications",
		# 	content=None,
		# 	reference_doctype=None,
		# 	reference_name=None,
		# 	message = frappe.render_template("templates/email/sales_invoice_sunmit_notification.html", {"name":doc.name,"customer":doc.customer}),
		# 	message_id=None,
		# 	unsubscribe_message=None,
		# 	delayed=False,
		# 	communication=None
		# )
		
		# except Exception,e:
		# 	frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))


@frappe.whitelist()
def get_sales_invoices():
	#sales_incoice = frappe.get_all("Sales Invoice",filters = [['status', '!=', 'Cancelled']])
	sales_incoice = frappe.db.sql(""" select name from `tabSales Invoice` where status != 'Cancelled' and name not in('SINV-00254','SINV-00296-1')""",as_dict=True)
	for invoice in sales_incoice:
		print "\n\n----------",invoice
		doc = frappe.get_doc("Sales Invoice",invoice.get('name'))
		if doc:
			discount_amount = delivery_charge = other_amount =0.0
	
			if doc.shipping_rule:
				shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
			''' Get Shipping Charges,VAT '''
			doc.printformat_vat_tax = None
			for tax in doc.taxes:
				# if doc.shipping_rule:
				# 	shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
				# 	if tax.account_head == shipping_rule_doc.account:
				# 		doc.delivery_charge = tax.tax_amount
				# 		tax.print_flag = 0

				if tax.account_head == "Output VAT  - E":
					doc.printformat_vat_tax = tax.tax_amount
					tax.print_flag = 0

				if doc.discount_amount:
					discount_amount = doc.discount_amount

			for tax in doc.taxes:
				if tax.print_flag ==1:
					other_amount = other_amount + tax.tax_amount
			doc.printformat_other_total = other_amount
			doc.printformat_net_total = (doc.total - doc.discount_amount) + flt(doc.printformat_other_total)
			doc.save(ignore_permissions = True)
			print "Done"





	