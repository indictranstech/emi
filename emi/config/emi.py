from frappe import _

def get_data():
	return [	
	{
		"label": _("Job Card"),
		"icon": "icon-star",
		"items": [
			{
				"type": "doctype",
				"name": "Job Card",
				"label": _("Job Card"),
				"description": _("Job Card")
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
				"name": "Vendor Evaluation",
				"description": _("Vendor Evaluation")
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
			"is_query_report": True,
			"name": "Production%20Status",
			"label": _("Production Status Report"),
			"description": _("Production Report (Process Wise)"),
			"doctype":"Job Card"
		},
		{
			"type": "report",
			"name": "Job Card Report",
			"label": _("Job Card Report"),
			"description": _("Production Report (Process Wise)"),
			"doctype":"Job Card"
		}
		]
	}
	]