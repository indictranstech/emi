


frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		
	},
	validate: function(frm) {
	  	var html = $(".tax-break-up").html()
	  	if (html)
	  	{
	  		frm.set_value("tax_breakup",html);
	  	}
	  	
	}
});