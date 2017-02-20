// Copyright (c) 2016, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Order', {
	refresh: function(frm) {
		cur_frm.add_fetch('production_order', 'qty', 'quantity');	
		cur_frm.add_fetch('production_order', 'production_item', 'item');
	},



});

frappe.ui.form.on('Job Order Detail',{
	completed_job:function(frm, cdt, cdn){
		var d = locals[cdt][cdn]
		console.log("d", d.completed_job,d.job_allocated && d.job_allocated < d.completed_job)
		if(d.job_allocated <= d.completed_job ){
			//console.log("please")
			d.completed_job=""
			frappe.throw("Please check the assigned Quantity not Greater than the Completed Qty");
		}
		
	},
	rejected_qty:function(frm, cdt, cdn){
		var d = locals[cdt][cdn]
		if(d.rejected_qty >= d.job_allocated){
			d.rejected_qty=""
			frappe.throw("Please check the assigned Quantity not Greater than the Completed Qty");
		}
	},

	job_order_detail_add: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		console.log(".....hi", d)
		d.job_order_id = "Job-"+ d.idx
		//job_order_id.refresh()
	}
	/*refresh:function(frm,cdt,cdn)
	{
		cur_frm.fields_dict['production_order'].get_query = function(doc) {
			return {
				query:"emi.emi.emi.doctype.job_order.job_order.get_info_production",
				console.log("hiiiiiiiiiiiiiii")
			}
		}

	}*/
});

cur_frm.fields_dict.job_order_detail.grid.get_field("production_order").get_query = function(doc) {
	return {
		filters: {
			"status": 'In Process'
		}
	}
}