from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr,get_datetime
from frappe import _

def on_submit(self, method=None):
	account_manager = frappe.db.sql("select parent from tabUserRole where role = 'Emi Account Manager' and parent <> 'Administrator'",as_dict=True)
	store_managers = frappe.db.sql("select parent from tabUserRole where role = 'Emi Store Manager' and parent <> 'Administrator'",as_dict=True)
	if account_manager:
		account_manager_list = [manager.get('parent') for manager in account_manager]
		if account_manager_list:
			for manager in account_manager_list:
				name = frappe.db.get_value("User",{"name":manager},"first_name")
				account_manger_notification(manager,name,self.name,self.customer,self.posting_date,self.total)	

	if store_managers:
		store_managers_list = [manager.get('parent') for manager in store_managers]
		if store_managers_list:
			for manager in store_managers_list:
				name = frappe.db.get_value("User",{"name":manager},"first_name")
				store_manger_notification(manager,name,self.name,self.customer,self.items,self.posting_date,name)

	for row in self.sales_team:
		if row:
			recipients =frappe.db.get_value("Employee",{'employee_name':row.sales_person},"user_id")	
			delivery_note_submit_notification(row.sales_person,self.name,row.allocated_amount,self.posting_date,recipients)			

def delivery_note_submit_notification(Name,name,amount,date,recipients):
	date = frappe.utils.get_datetime(date).strftime("%d-%m-%Y")
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
			message = frappe.render_template("templates/email/delivery_note_submit_sales_execute_notification.html", {"Name":Name,"name":name,"amount":amount,"date":date}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))


# # After Submitting Delivery Note Notification will be get sent to Account Manager
def account_manger_notification(recipients,Name,delivery_note,customer,date,amount):
	date = frappe.utils.get_datetime(date).strftime("%d-%m-%Y")
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

def store_manger_notification(recipients,Name,delivery_note,customer,items,date,name):
	date = frappe.utils.get_datetime(date).strftime("%d-%m-%Y")
	try:
		frappe.sendmail(
			recipients=recipients,
			expose_recipients="header",
			sender=frappe.session.user,
			reply_to=None,
			subject="Delivery Note Submit Notification For Store",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/delivery_note_store_manager.html",{"Name":Name,"name":delivery_note,"customer":customer,"items":items,"date":date,"name":name}),
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
			if float(row.idx) % 8 == 0 and row.idx > 8:
				row.page_break = 1

		

