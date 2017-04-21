// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.query_reports["Pending Purchase Order"] = {
	filters:[
				{
					"fieldname":"name",
					"label": __("Purchase Order"),
					"fieldtype": "Link",
					"options": "Purchase Order",
					"width": "80",
					"get_query": function() {
						return {
									"query": "emi.emi.doctype.job_card.job_card.purchase_order_query",
									"filters": [
												['Purchase Order', 'status', 'in', 'Draft,To Deliver and Bill ']
											]
								}
					}
					
				}
			]
}
