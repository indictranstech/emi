# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "emi"
app_title = "Emi"
app_publisher = "Indictranstech"
app_description = "Manufacturing Ladder"
app_icon = "octicon octicon-file-directory"
app_color = "Blue"
app_email = "sagar.s@indictranstech.com"
app_license = "INDICTRANS"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/emi/css/c3.css"
# app_include_js = "/assets/emi/js/c3.min.js"
# app_include_js = "/assets/js/telecom_v7.js"
# include js, css files in header of web template
# web_include_css = "/assets/emi/css/emi.css"
# web_include_js = "/assets/emi/js/emi.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "emi.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "emi.install.before_install"
# after_install = "emi.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "emi.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events


doc_events = {
	"Sales Invoice": {
		"validate": "emi.emi.custom_methods.validate_delivery_note",
	},

	('Quotation', 'Sales Order'): {
		"validate": "emi.emi.custom_methods.calulate_consolidated_margin"
	},
	"Stock Ledger Entry" :{
		"before_submit": "emi.emi.custom_methods.get_requested_for"
	},
	"Delivery Note": {
        "validate": "emi.custom_script.delivery_note.delivery_note.validate",
    },
	
}

doctype_js = {
    "Quotation":["custom_script/quotation/quotation.js"],
    "Sales Order" :["custom_script/sales_order/sales_order.js"]  
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"emi.tasks.all"
# 	],
# 	"daily": [
# 		"emi.tasks.daily"
# 	],
# 	"hourly": [
# 		"emi.tasks.hourly"
# 	],
# 	"weekly": [
# 		"emi.tasks.weekly"
# 	]
# 	"monthly": [
# 		"emi.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "emi.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "emi.event.get_events"
# }
fixtures = ["Web Form","Custom Field","Print Format","Property Setter","Letter Head","Report","Custom Script"]
