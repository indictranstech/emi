from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr,get_datetime
from frappe import _



def notify_to_qc_manager(doc, method=None):
	if doc.docstatus == 1:

		subject = "Quality Inspection {0} Submit Notification".format(doc.name)
		message = frappe.get_template("templates/email/qc_submit_notification_to_quality_manager.html").render({
			"name":doc.name,"inspection_type":doc.inspection_type,"reference_name":doc.reference_name,"reference_type":doc.reference_type,"report_date":doc.report_date,
			"item_code":doc.item_code,"item_name":doc.item_name,"inspected_by":doc.inspected_by,"verified_by":doc.verified_by_manager
		})
	if doc.verified_by_manager:
		verified_by = doc.verified_by_manager
		#frappe.sendmail(recipients=verified_by,subject=subject,message=message)

