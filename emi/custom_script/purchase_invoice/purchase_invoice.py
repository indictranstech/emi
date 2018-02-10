from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import flt, cint, nowdate,get_datetime
from frappe.utils import cstr
from frappe import _
from bs4 import BeautifulSoup
from frappe.utils import money_in_words

def PI_submit_notification(doc,method=None):
	if doc.docstatus == 1:
		try:
			frappe.sendmail(
			recipients=["sridhar@emiuae.ae","mathur@emiuae.ae","rahul.saharia@emiuae.ae"],
			#recipients=["onkar.m@indictranstech.com"],
			expose_recipients="header",
			# sender=frappe.session.user,
			# reply_to=None,
			subject="PurchaseInvoice Submit Notifications",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/purchase_invoice_sunmit_notification.html", {"name":doc.name}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
		
		except Exception,e:
			frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))
