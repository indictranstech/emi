from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr
from frappe import _

def validate(self, method=None):
	if self.docstatus == 0 and self.purpose == "Material Transfer":
		store_managers = frappe.db.sql(" select parent from tabUserRole where  role = 'Emi Store Manager' and parent <> 'Administrator'",as_list=True)
		if store_managers:
			for manager in store_managers[0]:
				name = frappe.db.get_value("User",{"name":manager},"first_name")
				stock_entry_submit_notification(self.name,manager,name,self.purpose,self.items)
	

def stock_entry_submit_notification(name,recp,recpname,purpose,items):
	date = str(frappe.utils.data.now_datetime())
	try:
		frappe.sendmail(
			recipients=recp,
			expose_recipients="header",
			sender=frappe.session.user,
			reply_to=None,
			subject="Material Transfer Notification for "+ name,
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/stock_entry.html", {"Name":recpname,"purpose":purpose,"items":items,"date":date}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))

