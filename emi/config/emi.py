from frappe import _

def get_data():
	return [	
	{
		"label": _("Purchase"),
		"icon": "icon-star",
		"items": [
			{
				"type": "doctype",
				"name": "Supplier",
				"label": _("Supplier"),
				"description": _("Supplier")
			},
			{
				"type": "doctype",
				"name": "Supplier Quotation",
				"label": _("Supplier Quotation"),
				"description": _("Supplier Quotation")
			},
			{
				"type": "doctype",
				"name": "Purchase Order",
				"label": _("Purchase Order"),
				"description": _("Purchase Order")
			},
			{
				"type": "doctype",
				"name": "Purchase Receipt",
				"label": _("Purchase Receipt"),
				"description": _("Purchase Receipt")
			},
		]
	},
	
	{
		"label": _("Sales"),
		"icon": "icon-star",
		"items": [
			{
				"type": "doctype",
				"name": "Customer",
				"label": _("Customer"),
				"description": _("Customer")
			},
			{
				"type": "doctype",
				"name": "Quotation",
				"label": _("Quotation"),
				"description": _("Quotation")
			},
			{
				"type": "doctype",
				"name": "Sales Order",
				"label": _("Sales Order"),
				"description": _("Sales Order")
			},
			{
				"type": "doctype",
				"name": "Delivery Note",
				"label": _("Delivery Note"),
				"description": _("Delivery Note")
			},
		]
	},
	{
		"label": _("Production"),
		"icon": "icon-star",
		"items": [
			{
				"type": "doctype",
				"name": "BOM",
				"label": _("BOM"),
				"description": _("BOM")
			},
			{
				"type": "doctype",
				"name": "Production Order",
				"label": _("Production Order"),
				"description": _("Production Order")
			},
			{
				"type": "doctype",
				"name": "Job Card",
				"label": _("Job Card"),
				"description": _("Job Card")
			},
			{
				"type": "doctype",
				"name": "Production Planning Tool",
				"label": _("Production Planning Tool"),
				"description": _("Production Planning Tool")
			},
		]
	},
	{
		"label": _("Stock"),
		"icon": "icon-star",
		"items": [
			{
				"type": "doctype",
				"name": "Item",
				"label": _("Item"),
				"description": _("Item")
			},
		]
	},
	{
		"label": _("Master Details"),
		"icon": "icon-star",
		"items": [
			{
				"type":"doctype",
				"name": "Machine",
				"description": _("Machine")
			},
			{
				"type":"doctype",
				"name": "Process",
				"description": _("Process")
			},	
	        {
				"type":"doctype",
				"name": "Sub Category",
				"description": _("Sub Category")
			},
			{
				"type":"doctype",
				"name": "Quality Report",
				"description": _("Quality Report")
			},
		]
	},
		
	{
	"label": _("Report"),
	"icon": "icon-star",
	"items": [
		{
			"type": "report",
			"is_query_report": True,
			"name": "Process%20wise%20Production%20Report",
			"label": _("Production Report (Process Wise)"),
			"description": _("Production Report (Process Wise)"),
			"doctype":"Job Card"
		},
		{
			"type": "report",
			"name": "Job%20Card%20Report",
			"label": _("Job Card Report"),
			"description": _("Job Card Report"),
			"doctype":"Job Card"
		}
		]
	}
	]