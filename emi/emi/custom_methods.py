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
	price_list_rate_sum = 0
	margin_sum = 0
	for row in doc.items:
		price_list_rate_sum += row.price_list_rate
		margin_sum += row.total_margin
	if margin_sum > 0:
		doc.consolidated_margin = margin_sum - price_list_rate_sum

