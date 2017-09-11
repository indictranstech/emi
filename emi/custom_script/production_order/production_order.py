from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr,get_datetime
from frappe import _

def notify_to_qty_manager(doc, method=None):
	if doc.status == "Completed":
		qty_manager = frappe.db.sql_list("""select parent FROM tabUserRole
			WHERE role="Emi Quality Manager"
			AND parent!='Administrator'
			AND parent IN (SELECT email FROM tabUser WHERE enabled=1)""")
		subject = "Production Order {0} Submit Notification".format(doc.name)
		message = frappe.get_template("templates/email/po_submit_notification.html").render({
			"name":doc.name
		})
		frappe.sendmail(recipients=qty_manager,subject=subject,message=message)