# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_colums(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if filters:
		if filters.sale_person and not filters.customer:
			data= frappe.db.sql("""select so.name,so.customer,so.transaction_date,so.delivery_date,so.grand_total,
					st.sales_person,st.contact_no,st.allocated_percentage,st.allocated_amount,
					st.incentives
					from
  						`tabSales Order` so, `tabSales Team` st
					where
 							st.parent =so.name and st.sales_person='{0}'
					order by so.name desc""".format(filters.sale_person),debug=1)
			return data
		if filters.customer and not filters.sale_person :
			data= frappe.db.sql("""select so.name,so.customer,so.transaction_date,so.delivery_date,so.grand_total,
					st.sales_person,st.contact_no,st.allocated_percentage,st.allocated_amount,
					st.incentives
					from
  						`tabSales Order` so, `tabSales Team` st
					where
 							st.parent =so.name and so.customer ='{0}'
					order by so.name desc""".format(filters.customer),debug=1)
			return data
		if filters.customer and  filters.sale_person :
			data= frappe.db.sql("""select so.name,so.customer,so.transaction_date,so.delivery_date,so.grand_total,
					st.sales_person,st.contact_no,st.allocated_percentage,st.allocated_amount,
					st.incentives
					from
  						`tabSales Order` so, `tabSales Team` st
					where
 							st.parent =so.name and st.sales_person='{0}' and so.customer ='{1}'
					order by so.name desc""".format(filters.sale_person,filters.customer),debug=1)
			return data

	

	else:
		data= frappe.db.sql("""select so.name,so.customer,so.transaction_date,so.delivery_date,so.grand_total,
					st.sales_person,st.contact_no,st.allocated_percentage,st.allocated_amount,
					st.incentives
					from
  						`tabSales Order` so, `tabSales Team` st
					where
 							st.parent =so.name 
					order by so.name desc""")
		print "***data",data
		return data 

def get_colums(filters):
	columns =[ ("Sales Order") + ":Link/Sales Order:100",
				   ("Party") + ":230",
				   ("Date") + ":100",
				   ("Delivary Date")+ ":100",
				   ("Sales Amount") + ":Currency:120",
				   ("Sales Person") + ":Data:120",
				   ("Contact No") + ":Data:120",
				   ("Allocated Percentage") + ":Data:120",
				   ("Allocated Amount") + ":Currency:120",
				   ("Incentives") + ":Data:120"


			]
	return columns
