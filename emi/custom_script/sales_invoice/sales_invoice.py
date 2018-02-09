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
	printformat_net_total = printformat_vat_tax = 0.0
	discount_amount = delivery_charge = 0.0
	for tax in doc.taxes:
		if tax.account_head == "Stock Adjustment - E":
			delivery_charge = tax.tax_amount

		if tax.account_head == "VAT 5% - E":
			doc.vat = tax.tax_amount

	if doc.discount_amount:
		discount_amount = doc.discount_amount
		
	printformat_net_total = (doc.total - discount_amount) + delivery_charge
	printformat_vat_tax = (printformat_net_total * 5)/100
	doc.printformat_net_total_with_tax = printformat_net_total + printformat_vat_tax
	doc.printformat_net_total = printformat_net_total
	doc.printformat_vat_tax = printformat_vat_tax
	doc.printformat_in_word = money_in_words(doc.printformat_net_total_with_tax, doc.currency)

def SI_submit_notification(doc,method=None):
	if doc.docstatus == 1:
		try:
			frappe.sendmail(
			#recipients=["sridhar@emiuae.ae","mathur@emiuae.ae"],
			recipients=["onkar.m@indictranstech.com"],
			expose_recipients="header",
			# sender=frappe.session.user,
			# reply_to=None,
			subject="Sales Invoice Submit Notifications",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/sales_invoice_sunmit_notification.html", {"name":doc.name,"customer":doc.customer}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
		
		except Exception,e:
			frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))


	
	




	