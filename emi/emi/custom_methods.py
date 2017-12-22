
import frappe
from frappe.utils import flt, cint, nowdate
from erpnext.stock.doctype.stock_entry.stock_entry import get_additional_costs


def validate_delivery_note(doc, method):
	#check submitted invoice against delivery note
	exist_invoice = frappe.db.get_value("Sales Invoice", 
			{ "delivery_note": doc.delivery_note, "docstatus": 1}, "name")
	if exist_invoice:
		frappe.throw("Sales Invoice <b>{0}</b> for Delivery Note <b>{1}</b> already created.". 
			format(exist_invoice, doc.delivery_note))
	
def calulate_consolidated_margin(doc, method):
	# Calculat consolidate_margin = sum of item_price_rate - sum of total_margin
	# Calculate price_list_total,and margin percentage
	#Page-break
	for row in doc.items:
		if len(doc.items) > 8:
			if float(row.idx) % 8 == 0:
				row.page_break = 1

	consolidated_margin = 0
	price_list_total = 0	
	discounted_amount = 0.0

	for row in doc.items:
		if not row.price_list_rate:
			frappe.throw(("First create 'Item Price' for this item."))
		if row.rate > row.price_list_rate and not row.margin_type:
			diff = row.rate -row.price_list_rate
			row.margin_type = "Amount"
			row.margin_rate_or_amount = flt(diff)
			row.total_margin = row.rate
			row.discount_percentage = 0.0

	for row in doc.items:
		if not row.price_list_rate:
			frappe.throw(("First create 'Item Price' for this item."))

		# # if row.discount_percentage:
		# # 	if row.margin_type == "Amount":	
		# # 		margin_price = float(row.margin_rate_or_amount)
		# # 		discount_price = float((row.total_margin*row.discount_percentage)/100)
		# # 		item_rate =row.total_margin -discount_price
		# # 		if discount_price >= margin_price and row.price_list_rate >= item_rate:
		# # 			frappe.throw(("You Can't Give " +str(row.discount_percentage)+" % Discount "))

		# # 	if row.margin_type == "Percentage":
		# # 		margin_price = float(((row.price_list_rate *row.margin_rate_or_amount)/100))
		# # 		discount_price = float((row.total_margin*row.discount_percentage)/100)
		# # 		item_rate =row.total_margin -discount_price
		# # 		if discount_price >= margin_price and row.price_list_rate >= item_rate :
		# # 			frappe.throw(("You Can't Give " +str(row.discount_percentage)+" % Discount "))
 
		# 	last_rate = (row.price_list_rate + (row.price_list_rate * 5)/100)
		# 	current_rate = row.rate
		# 	if current_rate < last_rate:
		# 		less_margin_notification(doc.doctype,doc.name,row.margin_rate_or_amount,row.margin_type,row.discount_percentage)

		if row.margin_rate_or_amount:
			if row.margin_type == "Percentage":		
				margin_amt = ((row.price_list_rate * row.margin_rate_or_amount)/100) * row.qty
				consolidated_margin += margin_amt
				price_list_total += (row.price_list_rate * row.qty)
				
			elif row.margin_type == "Amount":
				consolidated_margin += (row.margin_rate_or_amount * row.qty)
				price_list_total += (row.price_list_rate * row.qty)
				
		else:
			if row.rate < row.price_list_rate:
				if row.discount_percentage:
					discounted_amount = discounted_amount + ((row.price_list_rate -row.rate)*row.qty)
					price_list_total += (row.price_list_rate * row.qty)
					
				else:
					price_list_total += (row.price_list_rate * row.qty)

	doc.consolidated_margin = consolidated_margin
	doc.discounted_amount = discounted_amount
	doc.price_list_total = price_list_total
	
	if consolidated_margin != 0: 
		doc.consolidated_margin_percentage = get_percenage(float(consolidated_margin),float(price_list_total))
	if doc.apply_discount_on == "Net Total" and doc.additional_discount_percentage and doc.discount_amount:
		if doc.consolidated_margin != 0:
			doc.consolidated_margin = doc.consolidated_margin - doc.discount_amount
			doc.consolidated_margin_percentage = get_percenage(float(doc.consolidated_margin),float(price_list_total))
	if doc.doctype == "Sales Order" and doc.status == "To Deliver and Bill":
		sales_order_submit_notification(doc.name,doc.consolidated_margin_percentage)
	
	if doc.doctype == "Quotation" and doc.status == "Submitted":
		# sales_executives= frappe.db.sql(" select parent from tabUserRole where  role = 'Emi Sales Executive' and parent <> 'Administrator'",as_list=True)
		# if sales_executives:
		# 	for executive in sales_executives[0]:
		# 		name = frappe.db.get_value("User",{"name":executive},"first_name")
		# 		quotation_submit_notification(doc.name,doc.consolidated_margin_percentage,executive,name,doc.customer)	
		if doc.employee:
			email_id=frappe.db.get_value("Employee",{"name":doc.employee},"user_id")
			quotation_submit_notification(doc.name,doc.consolidated_margin_percentage,email_id,doc.lead_owner_name,doc.customer)

	if doc.consolidated_margin:
		if doc.discount_amount>doc.consolidated_margin:
			frappe.throw(("Discount Amount Should Be Less Than Consolidated Margin"))


"""Get requested_for field when update_stock is 1"""
def get_requested_for(self,method):
	if self.voucher_type == "Stock Entry":
		requested_for = frappe.db.get_value("Stock Entry",{"name":self.voucher_no},["requested_for"])
		self.requested_for = requested_for

def add_margin_price(items,final_margin_type,final_margin_rate_or_amount):
	for row in items:
		row.margin_type = final_margin_type
		row.margin_rate_or_amount = final_margin_rate_or_amount 

def get_percenage(value1,value2):
	return (value1/value2*100)

def sales_order_submit_notification(name,margin):
	try:
		frappe.sendmail(
			recipients=["david.newman@emiuae.ae","rachitsaharia@emiuae.ae"],
			#recipients=["onkar.m@indictranstech.com","khushal.t@indictranstech.com"],
			expose_recipients="header",
			# sender=frappe.session.user,
			# reply_to=None,
			subject="Sales Order Submit Notifications",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/sales_order_sunmit_notification.html", {"name":name,"margin":margin}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))

def quotation_submit_notification(name,margin,recp,recp_name,customer):
	try:
		frappe.sendmail(
			recipients = recp,
			expose_recipients = "header",
			sender = frappe.session.user,
			reply_to = None,
			subject = "Quotation Submit Notifications",
			content = None,
			reference_doctype = None,
			reference_name = None,
			message = frappe.render_template("templates/email/quotation_submit_notification.html", {"Name":recp_name,"name":name,"margin":margin,"customer":customer}),
			message_id = None,
			unsubscribe_message = None,
			delayed = False,
			communication = None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))

def SO_submit_notification_to_sales_person(name,recp,recp_name,customer):
	try:
		message = frappe.render_template("templates/email/SO_submit_notification_to_sales_person.html", {
			"Name":recp_name,"name":name,"customer":customer
		})
		subject="Sales Order Submit Notifications"
		frappe.sendmail(recipients=recp,subject=subject,message=message,delayed=False)
		
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))


def produ_order(self):
	black=frappe.db.get_value("Job Card",{"name":production_order},"black_material")


@frappe.whitelist()
def make_stock_entry(production_order_id, purpose, qty=None, name=None, via_job_card=False):
	production_order = frappe.get_doc("Production Order", production_order_id)

	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.purpose = purpose
	stock_entry.production_order = production_order_id
	stock_entry.company = production_order.company
	stock_entry.from_bom = 1
	stock_entry.bom_no = production_order.bom_no
	stock_entry.use_multi_level_bom = production_order.use_multi_level_bom
	stock_entry.fg_completed_qty = qty or (flt(production_order.qty) - flt(production_order.produced_qty))

	if purpose=="Material Transfer for Manufacture":
		if production_order.source_warehouse:
			stock_entry.from_warehouse = production_order.source_warehouse
		stock_entry.to_warehouse = production_order.wip_warehouse
		stock_entry.project = production_order.project
	else:
		stock_entry.from_warehouse = production_order.wip_warehouse
		stock_entry.to_warehouse = production_order.fg_warehouse
		additional_costs = get_additional_costs(production_order, fg_qty=stock_entry.fg_completed_qty)
		stock_entry.project = frappe.db.get_value("Stock Entry",{"production_order": production_order_id,"purpose": "Material Transfer for Manufacture"}, "project")
		stock_entry.set("additional_costs", additional_costs)

	stock_entry.get_items()
	if via_job_card or purpose == "Material Transfer for Manufacture":
		stock_entry.save(ignore_permissions=True)
		stock_entry.submit()
		if via_job_card:
			return production_order
	return stock_entry.as_dict()

def after_install_process_add():
	processes = ["Pre Inspection","Punching","Bending", "Cutting", "Welding","Shearing","Cleaning","Final Inspection","Programming","Custom 1","Custom 2","Reduced Bending","Drilling","Tapping","Rolling","Assembly","Powder Coating", "Hot Dip Galvanizing", "Wet Coating"]
	process = frappe.new_doc("Process")
	for p in processes: 
		if not frappe.db.exists("Process", p):
  			process.process = p
  			process.insert()

def after_install_warehouse_add():
	default_comp = frappe.defaults.get_defaults().get("company")
	if default_comp:
		default_abbr = frappe.db.get_value("Company",{"name":default_comp}, ["abbr"])
		warehouses = ["EMI","Factory Store Black","Factory Store Polish","Final Inspected Warehouse"]
	warehouse = frappe.new_doc("Warehouse")
 	for row in warehouses: 
		if not frappe.db.get_value("Warehouse",{"name": row + " - " + default_abbr}, "name"):
  			warehouse.warehouse_name = row
  			warehouse.parent_warehouse ="All Warehouses - " + default_abbr
  			warehouse.ignore_mandatory=True
  			warehouse.insert()

def send_email_sales_person(doc,method=None):
	if doc.doctype == "Sales Order" and doc.status == "To Deliver and Bill":
		# sales_order_submit_notification(doc.name,doc.consolidated_margin_percentage)
		if doc.employee:
			email_id=frappe.db.get_value("Employee",{"name":doc.employee},"user_id")
			SO_submit_notification_to_sales_person(doc.name,email_id,doc.lead_owner_name,doc.customer)

#Quoat Submitted send email to Sales Person
def send_email_sales_person_quot(doc,method=None):
	if doc.doctype == "Quotation" and doc.status == "Submitted":
		if doc.employee:
			email_id=frappe.db.get_value("Employee",{"name":doc.employee},"user_id")
			SO_submit_notification_to_sales_person(doc.name,email_id,doc.lead_owner_name,doc.customer)

def validate_si(doc, method):
	for row in doc.items:
		if len(doc.items) > 8:
			if float(row.idx) % 8 == 0:
				row.page_break = 1