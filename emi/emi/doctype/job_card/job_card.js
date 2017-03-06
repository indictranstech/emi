// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Card', {
	refresh: function(frm) {
		cur_frm.add_fetch('production_order', 'qty', 'quantity');	
		cur_frm.add_fetch('production_order', 'production_item', 'item');
		cur_frm.add_fetch('production_order', 'description', 'description');
	}
});

frappe.ui.form.on('Job Order Detail',{
	completed_job:function(frm, cdt, cdn){
		var d = locals[cdt][cdn]
		if(flt(d.job_allocated) < flt(d.completed_job) ){
			d.completed_job=""
			frappe.throw("Please check the Completed Quantity not Greater than the Assigned Qty");
		}
		
	},
	rejected_qty:function(frm, cdt, cdn){
		var d = locals[cdt][cdn]
		if(flt(d.job_allocated) < flt(d.rejected_qty)){
			d.rejected_qty=""
			frappe.throw("Please check the Rejected Quantity not Greater than the Assigned Qty");
		}
	},

	job_order_detail_add: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		d.job_order_id = "Job-"+ d.idx
		d.production_order=frm.doc.production_order
		d.item=frm.doc.item
		d.description=frm.doc.description
	}

});

cur_frm.fields_dict.job_order_detail.grid.get_field("production_order").get_query = function(doc) {
	return {
		filters: {
			"status": 'In Process'
		}
	}
}
cur_frm.fields_dict.job_order_detail.grid.get_field("machine_no").get_query = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return {
		filters: {
			"machine_no": d.process
		}
	}
}
cur_frm.fields_dict["production_order"].get_query = function(doc) {
	return {
		filters: {
			"status": 'In Process'
		}
	}
}
cur_frm.add_fetch('employee_name', 'employee_name', 'employee')
