// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Card', {
	refresh: function(frm) {
		cur_frm.add_fetch('production_order', 'qty', 'quantity');	
		cur_frm.add_fetch('production_order', 'production_item', 'item');
		cur_frm.add_fetch('production_order', 'description', 'description');
		cur_frm.add_fetch('production_order', 'sales_order', 'sales_order');
		cur_frm.add_fetch('production_order', 'requested_for', 'requested_for');
	},
	validate: function(frm) {
		var emp_mandatory_for = []
		var supplier_mandotory = []
		emp_processes = ["Pre Galvanize","Punching", "Cutting", "Welding","Shearing","Cleaning","Final Inspection"]
		supp_processes = ["Powder Coating", "Hot Dip Galvanizing", "Wet Coating"]
		$.each(frm.doc.job_order_detail, function(idx, row) {
			if (inList(emp_processes, row.process) && 
				(emp_mandatory_for.indexOf(row.process) == -1) &&
				!(row.employee_name)) {
				emp_mandatory_for.push(row.process)
			}
			if (inList(supp_processes, row.process) &&
				supplier_mandotory.indexOf(row.process) == -1 &&
				!(row.supplier)) {
				supplier_mandotory.push(row.process)
			}
		})
		if (supplier_mandotory.length) {
			frappe.throw("Supplier mandatory for processes: " + supplier_mandotory.join(","))		
		}
		if(emp_mandatory_for.length) {
			frappe.throw("Employee Name mandatory for processes: " + emp_mandatory_for.join(","))		
		}
	}
});

frappe.ui.form.on('Job Order Detail',{
	/*To Check completed_job Qty is not greater than Assigned Qty*/
	completed_job:function(frm, cdt, cdn){
		var d = locals[cdt][cdn]
		if(flt(d.job_allocated) < flt(d.completed_job) ){
			d.completed_job=""
			frappe.throw("Please check the Completed Quantity not Greater than the Assigned Qty");
		}
		
	},
	/*To Check Assigned Qty is not greater than Rejected Qty*/
	rejected_qty:function(frm, cdt, cdn){
		var d = locals[cdt][cdn]
		if(flt(d.job_allocated) < flt(d.rejected_qty)){
			d.rejected_qty=""
			frappe.throw("Please check the Rejected Quantity not Greater than the Assigned Qty");
		}
	},
	/*To Add Details Parent to Child Table  */
	job_order_detail_add: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		d.job_order_id = "Job-"+ d.idx
		d.production_order=frm.doc.production_order
		d.item=frm.doc.item
		d.description=frm.doc.description
		d.production_order_quantity=frm.doc.quantity
		d.sales_order=frm.doc.sales_order																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																															
	},
	/*To Check Final Inspection Process is not greater than one*/
	process: function(frm, cdt, cdn) {
	var counter=0;
	$.each(cur_frm.doc.job_order_detail,function(i,v){
		if(v.process=='Final Inspection'){
			counter++;
			if(counter>1){
				frappe.throw("Only One Final Inspection Process is Allowed in One Job Card")
			}
		}
	})
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


