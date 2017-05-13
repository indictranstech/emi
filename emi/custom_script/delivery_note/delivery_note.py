from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr
from frappe import _

def validate(self, method=None):
	#if self.status == "Completed":
	account_manager= frappe.db.sql(" select parent from tabUserRole where  role = 'Emi Account Manager' and parent <> 'Administrator'",as_list=True)
	if account_manager:
		for manager in account_manager[0]:
			print manager,type(manager)
			name = frappe.db.get_value("User",{"name":manager},"first_name")
			account_manger_notification(manager,name,self.name,self.customer,self.posting_date,self.total)	

	for row in self.sales_team:
		if row:
			recipients =frappe.db.get_value("Employee",{'employee_name':row.sales_person},"user_id")		
			delivery_note_submit_notification(row.sales_person,self.name,row.allocated_amount,recipients)			

def delivery_note_submit_notification(Name,delivery_note,amount,recipients):
	try:
		frappe.sendmail(
			recipients=recipients,
			expose_recipients="header",
			sender=frappe.session.user,
			reply_to=None,
			subject="Delivery Note Submit Notification",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/delivery_note_submit_sales_execute_notification.html", {"Name":Name,"name":delivery_note,"amount":amount}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))


# After Submitting Delivery Note Notification will be get sent to Account Manager
def account_manger_notification(recipients,Name,delivery_note,customer,date,amount):
	try:
		frappe.sendmail(
			recipients=recipients,
			expose_recipients="header",
			sender=frappe.session.user,
			reply_to=None,
			subject="Delivery Note Submit Notification",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/account_manager_notification.html",{"Name":Name,"name":delivery_note,"customer":customer,"date":date,"amount":amount}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))