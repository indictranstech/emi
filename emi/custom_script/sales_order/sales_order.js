
cur_frm.add_fetch("employee", "cell_number", "mobile_no");
cur_frm.add_fetch("employee", "employee_name", "lead_owner_name");

cur_frm.cscript.final_margin_type = function(frm){
	cur_frm.set_value("final_margin_rate_or_amount", 0.0)
	refresh_field("final_margin_rate_or_amount")
}

cur_frm.cscript.final_margin_rate_or_amount = function(frm){
	if (cur_frm.doc.final_margin_type == "Percentage"){
		// if (cur_frm.doc.final_margin_rate_or_amount == 0.000 || cur_frm.doc.final_margin_rate_or_amount == 0.0 || cur_frm.doc.final_margin_rate_or_amount == 0.00 ){
		// 	frappe.msgprint("You Cant Give Percentage As 0.0%")
		// }
	
	}
	$.each(cur_frm.doc.items, function(idx, val){
		val.margin_type = cur_frm.doc.final_margin_type
		val.margin_rate_or_amount = cur_frm.doc.final_margin_rate_or_amount
		console.log("val.name",val.name,"val.doctype",val.doctype)
		frappe.model.set_value(val.doctype, val.name, "margin_type",cur_frm.doc.final_margin_type);
		frappe.model.set_value(val.doctype, val.name, "margin_rate_or_amount",cur_frm.doc.final_margin_rate_or_amount);
		
		})
	refresh_field("items") 
}
 
frappe.ui.form.on('Sales Order Item',{
	items_add: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		d.margin_type = cur_frm.doc.final_margin_type;
		d.margin_rate_or_amount = cur_frm.doc.final_margin_rate_or_amount;
		refresh_field("items");
	}
	// qty: function(frm, cdt, cdn) {
	// 	$.each(cur_frm.doc.items, function(idx, val) {
	// 		frappe.model.set_value(val.doctype, val.name, "margin_type",cur_frm.doc.final_margin_type);
	// 		frappe.model.set_value(val.doctype, val.name, "margin_rate_or_amount",cur_frm.doc.final_margin_rate_or_amount);
	// 	})
	// }
	// rate:function(frm,cdt,cdn){
	// 	var d =  locals[cdt][cdn];
	// 	if (parseFloat(d.rate) > parseFloat(d.price_list_rate)){
	// 		var diff = (d.rate - d.price_list_rate);
	// 		frappe.model.set_value(d.doctype,d.name, "margin_type","Amount");
	//  		frappe.model.set_value(d.doctype,d.name, "margin_rate_or_amount",diff);
	//  		console.log("_______")
	//  		refresh_field("items");
	// 	}


	// }

});	
	
cur_frm.fields_dict['employee'].get_query = function(doc,cdt,cdn) {
	return{
			query: "emi.custom_script.sales_order.sales_order.get_sales_person",
			filters:{'customer': doc.customer}
	}
},

cur_frm.fields_dict.lead_owner_name.get_query = function(doc,cdt,cdn) {
	return{
		filters:{'customer': doc.customer}
	}
}

cur_frm.fields_dict['project'].get_query = function(doc, cdt, cdn) {
	return {
		query: "erpnext.controllers.queries.get_project_name",
		filters: {
			
		}
	}
}

frappe.ui.form.on('Sales Order', {
	onload: function(frm) {
		if(frappe.get_prev_route()[1]!="Quotation" && cur_frm.doc.__islocal)
		{
			frm.set_value("employee","")
		}
	},
})