import frappe

def validate_delivery_note(doc, method):
	#check submitted invoice against delivery note
	exist_invoice = frappe.db.get_value("Sales Invoice", 
			{ "delivery_note": doc.delivery_note, "docstatus": 1}, "name")
	if exist_invoice:
		frappe.throw("Sales Invoice <b>{0}</b> for Delivery Note <b>{1}</b> already created.". 
			format(exist_invoice, doc.delivery_note))
	
def calulate_consolidated_margin(doc, method):
	#calculat consolidate_margin = sum of item_price_rate - sum of total_margin
	# Calculate price_list_total,and margin percentage

	consolidated_margin = 0
	price_list_total = 0

	for row in doc.items:
		if not row.price_list_rate:
			frappe.throw(("Please Provide Prcie To Item First By Price List"))

		if row.discount_percentage:
			last_rate = (row.price_list_rate + (row.price_list_rate * 5)/100)
			current_rate = row.rate
			if current_rate < last_rate:
				less_margin_notification(doc.doctype,doc.name,row.margin_rate_or_amount,row.margin_type,row.discount_percentage)

		if row.margin_rate_or_amount:
			if row.margin_type == "Percentage":
				margin_amt = ((row.price_list_rate * row.margin_rate_or_amount)/100) * row.qty
				consolidated_margin += margin_amt
				price_list_total += row.price_list_rate * row.qty
			elif row.margin_type == "Amount":
				consolidated_margin += (row.margin_rate_or_amount * row.qty)
				price_list_total += row.price_list_rate * row.qty
	
	doc.consolidated_margin = consolidated_margin
	print "price_list_total",price_list_total
	if consolidated_margin != 0: 
		print "consolidated_margin_percentage",((consolidated_margin)/price_list_total*100)	
		doc.consolidated_margin_percentage = get_percenage(float(consolidated_margin),float(price_list_total))
	
	if doc.doctype ==  "Sales Order" and doc.status =="Submitted":
		sales_order_submit_notification(doc.name,doc.consolidated_margin_percentage)
		


"""Get requested_for field when update_stock is 1"""
def get_requested_for(self,method):
	if self.voucher_type == "Stock Entry":
		requested_for = frappe.db.get_value("Stock Entry",{"name":self.voucher_no},["requested_for"])
		self.requested_for = requested_for

def add_margin_price(items,final_margin_type,final_margin_rate_or_amount):
	for row in items:
		print row.idx 
		row.margin_type = final_margin_type
		row.margin_rate_or_amount = final_margin_rate_or_amount 

def get_percenage(value1,value2):
	return (value1/value2*100)

@frappe.whitelist()
def less_margin_notification(doctype,name,margin,margin_type,discount_percentage):
	frappe.sendmail(
				recipients="sagar.s@indictranstech.com",
				sender=frappe.session.user,
				subject="Low Magin",
				message=frappe.render_template("templates/email/less_margin_notification.html", {"Name":"Sagar","doctype": doctype,"name":name,"margin":margin,"type":margin_type,"discount":discount_percentage}) 
		)

def sales_order_submit_notification(name,margin):
	try:
		frappe.sendmail(
			recipients="sagar.s@indictranstech.com",
			expose_recipients="header",
			sender=frappe.session.user,
			reply_to=None,
			subject="Sales Order Submit Notifications",
			content=None,
			reference_doctype=None,
			reference_name=None,
			message = frappe.render_template("templates/email/sales_order_sunmit_notification.html", {"Name":"Sagar","name":name,"margin":margin}),
			message_id=None,
			unsubscribe_message=None,
			delayed=False,
			communication=None
		)
	except Exception,e:
		frappe.throw(("Mail has not been Sent. Kindly Contact to Administrator"))

def produ_order(self):
	black=frappe.db.get_value("Job Card",{"name":production_order},"black_material")
	print("Jjjjjjjjjjjjjjjj",black)