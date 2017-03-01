// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor Evaluation', {
	refresh: function(frm) {

		

	}

});

cur_frm.add_fetch('supplier', 'supplier_name', 'supplier');
cur_frm.add_fetch('supplier', 'nature_of_business', 'nature_of_business');
cur_frm.add_fetch('Supplier', 'website', 'website');
cur_frm.add_fetch('supplier', 'branch', 'branch');
cur_frm.add_fetch('supplier', 'bank_account_no', 'bank_account_no');
cur_frm.add_fetch('supplier', 'account_name', 'account_name');
cur_frm.add_fetch('supplier', 'bank_country', 'bank_country');
cur_frm.add_fetch('supplier', 'address', 'address');
cur_frm.add_fetch('supplier', 'swift_code', 'swift_code');
cur_frm.add_fetch('supplier', 'region', 'region');
cur_frm.add_fetch('supplier', 'bank_name', 'bank_name');
cur_frm.add_fetch('supplier', 'country', 'country');