from __future__ import unicode_literals
import frappe
from frappe import _, msgprint


@frappe.whitelist()
def get_data(from_date,to_date):

	data1 = frappe.db.sql("""select name,status,production_item from `tabProduction Order` """,as_dict=1)
	print 'data1',data1,"\n\n\n\n\n"
	
	

	t_count = len(data1)
	w_count = sum(li['status'] == "In Process" for li in data1)
	nw_count = sum(li['status'] == "Completed" for li in data1)
	um_count = sum(li['status'] == "Cancelled" for li in data1)
	# r_count = sum(li['status'] == "Retired" for li in data1)




	d = {'total_count':{},
		'working':{},
		'non_workinng':{},
		'under_maintenance':{},
		# 'retired':{},

		}

	d['total_count'].update({'count':t_count})
	d['working'].update({'count':w_count})
	d['non_workinng'].update({'count':nw_count})
	d['under_maintenance'].update({'count':um_count})
	# d['retired'].update({'count':r_count})

	

	print 'count',d,"\n\n\n\n\n"
	return d

