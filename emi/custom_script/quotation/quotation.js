
// cur_frm.cscript.margin_rate_or_amount = function(frm){
// 	$.each(cur_frm.doc.items, function(idx, val){
// 		val.margin_type = cur_frm.doc.margin_type
// 		val.margin_rate_or_amount = cur_frm.doc.margin_rate_or_amount
// 		/*frappe.model.set_value(cdt, cdn, "margin_type",doc.margin_type);*/
// 		})
// 	refresh_field("items") 
// }
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
		/*frappe.model.set_value(cdt, cdn, "margin_type",doc.margin_type);*/
		})
	refresh_field("items") 
}

frappe.ui.form.on('Quotation Item',{
	items_add: function(frm,cdt,cdn){	
		var d  = locals[cdt][cdn]
		d.margin_type = cur_frm.doc.final_margin_type
		d.margin_rate_or_amount =cur_frm.doc.final_margin_rate_or_amount
		refresh_field("items")
	},
	qty: function(frm, cdt, cdn) {
		$.each(cur_frm.doc.items, function(idx, val) {
			frappe.model.set_value(val.doctype, val.name, "margin_type",cur_frm.doc.final_margin_type);
			frappe.model.set_value(val.doctype, val.name, "margin_rate_or_amount",cur_frm.doc.final_margin_rate_or_amount);
		})
		refresh_field("items") 
	}
});



/*Project Filter on Customer Base*/
/*cur_frm.fields_dict['project'].get_query = function(doc,cdt,cdn) {
	return{
		filters:{ 
			'customer': doc.customer,
		}
	}
},*/

/*cur_frm.cscript.customer = function(frm){
console.log("hiiiiii")
return{
		query: "emi.custom_script.quotation.quotation.get_sales_person",
	}
	
}*/

cur_frm.fields_dict['employee'].get_query = function(doc,cdt,cdn) {
	return{
			query: "emi.custom_script.quotation.quotation.get_sales_person",
			filters:{'customer': doc.customer}
	}
},

cur_frm.fields_dict.lead_owner_name.get_query = function(doc,cdt,cdn) {
	return{
		//query: "emi.custom_script.quotation.quotation.get_sales_person",
		filters:{'customer': doc.customer}
}
}

frappe.ui.form.on('Quotation', {
	onload: function(frm) {
		if(cur_frm.doc.__islocal)
		{
			frm.set_value("employee","")
		}
	},
})