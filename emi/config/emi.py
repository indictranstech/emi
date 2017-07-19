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
			{
				"type": "doctype",
				"name": "Brand",
				"label": _("Category"),
				"description": _("Category")
			},
			{
				"type": "doctype",
				"name": "Sub Category",
				"label": _("Sub Category"),
				"description": _("Sub Category")
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
			"name": "Production%20Report%20(Process%20Wise)",
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
		},
		{
			"type": "report",
			"name": "Quality Inspect Report",
			"label": _("Quality Inspect Report"),
			"description": _("Quality Inspect Report"),
			"doctype":"Quality Report"
		},
		{
			"type": "report",
			"name": "Sales Analysis",
			"is_query_report": True,
			"label": _("Sales Analysis"),
			"description": _("Sales Analysis"),
			"doctype":"Sales Order"
		},
		{
			"type": "report",
			"name": "Sales Report For Sales Person Customer",
			"is_query_report": True,
			"label": _("Sales Report For Sales Person Customer"),
			"description": _("Sales Report For Sales Person Customer"),
			"doctype":"Sales Order"
		},
			{
			"type": "report",
			"name": "EMI Stock Balance",
			"is_query_report": True,
			"label": _("EMI Stock Balance"),
			"description": _("EMI Stock Balance"),
			"doctype":"Stock Ledger Entry"
		},
		]
	},
	{
	"label": _("Other Report"),
	"icon": "icon-star",
	"items": [
		{
			"type": "report",
			"name": "Item Shortage Report With Raw Material",
			"is_query_report": True,
			"label": _("Item Shortage Report With Raw Material"),
			"description": _("Item Shortage Report With Raw Material"),
			"doctype":"Bin"
		},
		{
			"type": "report",
			"name": "Item%20BOM%20Details",
			"is_query_report": True,
			"label": _("BOM Details Item Wise"),
			"description": _("BOM Details Item Wise"),
			"doctype":"Item"
			
		},
		{
			"type": "report",
			"name": "Quality Inspect Report",
			"label": _("Quality Inspect Report"),
			"description": _("Quality Inspect Report"),
			"doctype":"Quality Report"
		},
		{
			"type": "report",
			"name": "Pending%20Purchase%20Order",
			"is_query_report": True,
			"label": _("Pending Purchase Report"),
			"description": _("Pending Purchase Report"),
			"doctype":"Purchase Order"
		},
		{
			"type": "report",
			"name": "Pending%20Sales%20Order",
			"is_query_report": True,
			"label": _("Pending Sales Report"),
			"description": _("Pending Sales Report"),
			"doctype":"Sales Order"
		},
		{
			"type": "report",
			"name": "Margin%20per%20Sales%20Order",
			"label": _("Margin per Sales Order"),
			"description": _("Margin per Sales Order"),
			"doctype":"Sales Order"
		}
		]
	}
	]
	