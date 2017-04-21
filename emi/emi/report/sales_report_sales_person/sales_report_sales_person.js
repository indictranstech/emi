// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Report Sales Person"] = {
	"filters": [
			{
					"fieldname":"sale_person",
					"label": __("Sale Person"),
					"fieldtype": "Link",
					"options": "Sales Person",
					"width": "80",
					
			},

	]
}
