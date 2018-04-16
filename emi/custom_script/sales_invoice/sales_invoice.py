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
	discount_amount = delivery_charge = 0.0
	
	if doc.shipping_rule:
		shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
	''' Get Shipping Charges,VAT '''
	
	for tax in doc.taxes:
		if doc.shipping_rule:
			shipping_rule_doc = frappe.get_doc("Shipping Rule",doc.shipping_rule)
			if tax.account_head == shipping_rule_doc.account:
				doc.delivery_charge = tax.tax_amount

		if tax.account_head == "Output VAT  - E":
			doc.printformat_vat_tax = tax.tax_amount

	doc.printformat_net_total = (doc.total - doc.discount_amount) + flt(doc.delivery_charge)

def SI_submit_notification(doc,method=None):
	if doc.docstatus == 1:
		try:
			frappe.sendmail(
			recipients=["sridhar@emiuae.ae","mathur@emiuae.ae"],
			#recipients=["onkar.m@indictranstech.com"],
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


	
	




	