from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr,get_datetime
from frappe import _

def on_submit(self, method=None):
	store_managers = frappe.db.sql("select parent from tabUserRole where role = 'Emi Store Manager' and parent <> 'Administrator'",as_dict=True)
	if store_managers:
		store_managers_list = [manager.get('parent') for manager in store_managers]
		if store_managers_list:
			for manager in store_managers_list:
				name = frappe.db.get_value("User",{"name":manager},"first_name")
				purchase_receipt_submit_notification(self.name,manager,name,self.items,self.posting_date,self.supplier)

def purchase_receipt_submit_notification(name,recp,recpname,items,date,supplier):
	date = frappe.utils.get_datetime(date).strftime("%d-%m-%Y")
	try:
		frappe.sendmail(
			recipients=recp,
			expose_recipients="header",
			sender=frappe.session.user,
			reply_to=None,
			subject="Purchase Receipt Notification for "+ name,
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/purchase_receipt_notification.html", {"Name":recpname,"items":items,"date":date,"supplier":supplier}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))

def validate(self,method=None):
	
	for row in self.items:
		if len(self.items) > 8:
			if float(row.idx) % 8 == 0:
				row.page_break = 1