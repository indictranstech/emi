// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.query_reports["Item Shortage Report With Raw Material"] = {
	"filters": [
			{
					"fieldname":"item_code",
					"label": __("item_code"),
					"fieldtype": "Link",
					"options": "Item",
					"width": "80",
					"get_query": function() {
						return {
								"query": "emi.emi.doctype.job_card.job_card.product_query",
								
							}
				
					}
				}

	]
}
