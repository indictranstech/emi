// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quality Report', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__('Get Items From SO'),
			function() {
				erpnext.utils.map_current_doc({
					method: "emi.emi.doctype.quality_report.quality_report.get_so_items",
					source_doctype: "Sales Order",
					get_query_filters: {
						name:cur_frm.doc.so
					}
				})
			})
	},
});
