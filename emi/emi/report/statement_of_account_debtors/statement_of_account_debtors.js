// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.query_reports["Statement Of Account Debtors"] = {
	"filters": [
			{
				"fieldname":"company",
				"label": __("Company"),
				"fieldtype": "Link",
				"options": "Company",
				"default": frappe.defaults.get_user_default("Company")
			},
			{
				"fieldname":"customer",
				"label": __("Customer"),
				"fieldtype": "Link",
				"options": "Customer",
				change : function(){
					frappe.query_reports["Statement Of Account Debtors"].get_address($(this).val())
				}
			},
			{
				"fieldname":"report_date",
				"label": __("As on Date"),
				"fieldtype": "Date",
				"default": get_today()
			},
			{
				"fieldname":"ageing_based_on",
				"label": __("Ageing Based On"),
				"fieldtype": "Select",
				"options": 'Posting Date' + NEWLINE + 'Due Date',
				"default": "Posting Date"
			},
			{
				"fieldtype": "Break",
			},
			{
				"fieldname":"range1",
				"label": __("Ageing Range 1"),
				"fieldtype": "Int",
				"default": "30",
				"reqd": 1
			},
			{
				"fieldname":"range2",
				"label": __("Ageing Range 2"),
				"fieldtype": "Int",
				"default": "60",
				"reqd": 1
			},
			{
				"fieldname":"range3",
				"label": __("Ageing Range 3"),
				"fieldtype": "Int",
				"default": "90",
				"reqd": 1
			}
		],
		onload : function(report){
			this.report_data = report;
		},
		get_address: function(customer){
			var me =this;
			frappe.call({
					method: "emi.emi.report.statement_of_account_debtors.statement_of_account_debtors.get_address",
					args: {
						"customer": customer
					},
					callback: function(r, rt) {
						if(r.message) {
							me.report_data.address = r.message.addr
							me.report_data.cr_limit = r.message.cr_limit
							me.report_data.cr_days = r.message.cr_days
						}
					}
				});
		}

}
