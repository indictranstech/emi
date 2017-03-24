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
	consolidated_margin = 0
	for row in doc.items:
		if row.margin_rate_or_amount:
			if row.margin_type == "Percentage":
				margin_amt = (row.price_list_rate * (row.margin_rate_or_amount/100)) * row.qty
				consolidated_margin += margin_amt
			elif row.margin_type == "Amount":
				consolidated_margin += (row.margin_rate_or_amount * row.qty)
	doc.consolidated_margin = consolidated_margin



