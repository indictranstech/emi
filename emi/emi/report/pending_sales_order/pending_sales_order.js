// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Sales Order"] = {
	"filters": [
				{
					"fieldname":"name",
					"label": __("Sales Order"),
					"fieldtype": "Link",
					"options": "Sales Order",
					"width": "80",
					"get_query": function() {
					return {
								"query": "emi.emi.doctype.job_card.job_card.sales_order_query",
								"filters": [
										['Sales Order', 'status', 'in', 'Draft,To Deliver and Bill ']
								]
							}
					}
				},
				{
					"fieldname":"customer",
					"label": __("Customer"),
					"fieldtype": "Link",
					"options": "Customer",
					"width": "80",
					
				}
			]
}
