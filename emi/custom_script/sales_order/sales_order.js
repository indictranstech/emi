cur_frm.cscript.final_margin_type = function(frm){
	cur_frm.set_value("final_margin_rate_or_amount", 0.0)
	refresh_field("final_margin_rate_or_amount")
}

cur_frm.cscript.final_margin_rate_or_amount = function(frm){
	if (cur_frm.doc.final_margin_type == "Percentage"){
		if (cur_frm.doc.final_margin_rate_or_amount == 0.000 || cur_frm.doc.final_margin_rate_or_amount == 0.0 || cur_frm.doc.final_margin_rate_or_amount == 0.00 ){
			frappe.msgprint("You Cant Give Percentage As 0.0%")
		}
	
	}
	$.each(cur_frm.doc.items, function(idx, val){
		val.margin_type = cur_frm.doc.final_margin_type
		val.margin_rate_or_amount = cur_frm.doc.final_margin_rate_or_amount
		frappe.model.set_value(val.doctype, val.name, "margin_type",cur_frm.doc.final_margin_type);
		frappe.model.set_value(val.doctype, val.name, "margin_rate_or_amount",cur_frm.doc.final_margin_rate_or_amount);
		
		})
	refresh_field("items") 
}



 
frappe.ui.form.on('Sales Order Item',{
	items_add: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn]
		d.margin_type = cur_frm.doc.final_margin_type
		d.margin_rate_or_amount =cur_frm.doc.final_margin_rate_or_amount
		refresh_field("items")
	}
});

