import frappe

def validate_delivery_note(doc, method):
	exist_invoice = frappe.db.get_value("Sales Invoice", 
			{ "delivery_note": doc.delivery_note, "docstatus": 1}, "name")
	if exist_invoice:
		frappe.throw("Sales Invoice <b>{0}</b> for Delivery Note <b>{1}</b> already created.". 
			format(exist_invoice, doc.delivery_note))
	
	def calulate_consolidated_margin(doc):
		price_list_rate_sum = 0
		margin_sum = 0
		for row in doc.items():
			price_list_rate_sum += row.base_price_list_rate or 0
			margin_sum += row.total_margin or 0

