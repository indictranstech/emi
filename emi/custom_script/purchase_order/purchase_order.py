from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr,get_datetime
from frappe import _
from frappe.utils import money_in_words


@frappe.whitelist()
def validate(self,method=None):
	# for row in self.items:
	# 	if len(self.items) > 8:
	# 		if float(row.idx) % 8 == 0:
	# 			row.page_break = 1

	printformat_net_total = printformat_vat_tax = 0.0
	discount_amount = delivery_charge = 0.0

	for tax in self.taxes:
		if tax.account_head == "Stock Adjustment - E":
			delivery_charge = tax.tax_amount
	if self.discount_amount:
		discount_amount = self.discount_amount

	self.delivery_charge = delivery_charge
	printformat_net_total = (self.total - discount_amount) + delivery_charge
	printformat_vat_tax = (printformat_net_total * 5)/100
	self.printformat_net_total_with_tax = printformat_net_total + printformat_vat_tax
	self.printformat_net_total = printformat_net_total
	self.printformat_vat_tax = printformat_vat_tax
	self.printformat_in_word = money_in_words(self.printformat_net_total_with_tax, self.currency)

	page_break_idx = 8
	for row in self.items:
		if len(self.items)>7:
			if row.idx == 8:
				row.page_break = 1
				page_break_idx = 8
				page_break_idx += 15
			elif row.idx >= page_break_idx:
				if row.idx == page_break_idx:
					row.page_break = 1
					page_break_idx += 15	

@frappe.whitelist()
# def po_submit_notification ():
def po_submit_notification (self,method=None):
	if self.docstatus == 1:
		pass
		# try:
		# 	frappe.sendmail(
		# 	recipients=["rahul.saharia@emiuae.ae"],
		# 	#recipients=["onkar.m@indictranstech.com"],
		# 	expose_recipients="header",
		# 	# sender=frappe.session.user,
		# 	# reply_to=None,
		# 	subject="Purchase Order Submit Notifications",
		# 	content=None,
		# 	reference_doctype=None,
		# 	reference_name=None,
		# 	message = frappe.render_template("templates/email/purchase_order_submit_notification.html", {"name":self.name,"supplier":self.supplier}),
		# 	message_id=None,
		# 	unsubscribe_message=None,
		# 	delayed=False,
		# 	communication=None
		# )
		
		# except Exception,e:
		# 	frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))
