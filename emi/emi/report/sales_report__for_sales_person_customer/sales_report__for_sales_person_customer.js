// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Report  For Sales Person Customer"] = {
	"filters": [
			{
					"fieldname":"sale_person",
					"label": __("Sale Person"),
					"fieldtype": "Link",
					"options": "Sales Person",
					"width": "80",			
			},
			{
					"fieldname":"customer",
					"label": __("Customer"),
					"fieldtype": "Link",
					"options": "Customer",
					"width": "80",		
			},

	]
}
