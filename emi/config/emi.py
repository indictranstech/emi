from frappe import _

def get_data():
	return [	
	{
			"label": _("EMI Dashbords"),
			"icon": "icon-star",
			"items": [
				{
					"type": "page",
					"name": "dashboard",
					"label": _("Dashboard"),
					"icon": "icon-bar-chart",
					"description": _("Dashboard")
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
			]
		},
			{
			"label": _("Job Order"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Job Order",
					"label": _("Job Order"),
					"description": _("Job Order")
				},
			]
		}
	]