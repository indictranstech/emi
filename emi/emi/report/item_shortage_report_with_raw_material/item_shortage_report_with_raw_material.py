# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns =[ 
			   ("Product") + ":Data:110",
			   ("Qty To Produce") + ":Data:160",
			   ("Item Code") + ":Data:110",
			   ("Qty For Per Product") +":Data:130",
			   ("Actual Qty") + ":Data:110",
			   ("Ordered Qty") + ":Data:110",
			   ("Planned Qty") + ":Data:110",
			   ("Reserved Qty") + ":Data:110",
			   ("Projected Qty") + ":Data:110",
 
			 ]

	return columns
def get_data(filters):
	if filters:
		data=[];
		product_rsrd_qty =0.0;
		raw_rsrd_qty = 0.0;
		flag = 0
		default_bom = frappe.db.get_value("Item",{'item_code':filters.item_code},"default_bom")
		product_rsrd_qty = frappe.db.sql("""select reserved_qty from tabBin where item_code ='{0}'""".format(filters.item_code),as_list=1)
		if default_bom:
			bom_doc = frappe.get_doc("BOM",default_bom)
			items = bom_doc.items
			for row in items:
				qty = float(row.qty)
				raw_rsrd_qty = product_rsrd_qty[0][0] * float(row.qty);
				data1 =[[filters.item_code,product_rsrd_qty,row.item_code,row.qty,0.0, 0.0,0.0,raw_rsrd_qty,0.0]]
				qty_data = frappe.db.sql(""" select bn.warehouse,bn.item_code,bn.actual_qty,bn.ordered_qty,bn.planned_qty,
											 bn.reserved_qty,bn.projected_qty from tabBin bn where bn.item_code ='{0}'""".format(row.item_code),as_list=1,debug=1)
				for qty in qty_data:
					data1[0][4]=float(data1[0][4])+float(qty[2])   #actual_qty '''
					data1[0][5]=float(data1[0][5])+float(qty[3])   # ordered_qty"
					data1[0][6]=float(data1[0][6])+float(qty[4])   #planed_qty" 
					# data1[0][7]=float(data1[0][7])+float(qty[5])   #reserved_qty"
					data1[0][8]=float(data1[0][4])-float(data1[0][7])  #projected_qty"
				
				if float(data1[0][8]) <= 0.0:
				print "-knndvmkv"	
					data.extend(data1)
		return data
	else:
		products = frappe.db.sql("select bin.item_code from tabBin bin,tabItem i where bin.projected_qty <0 and i.item_code =bin.item_code and i.item_group ='Products'",as_dict=1)
		data =[]
		product_rsrd_qty =0.0;
		raw_rsrd_qty = 0.0;
		for product in products:
			default_bom = frappe.db.get_value("Item",{'item_code':product['item_code']},"default_bom")
			product_rsrd_qty = frappe.db.sql("""select reserved_qty from tabBin where item_code ='{0}'""".format(product['item_code']),as_list=1)
			if product_rsrd_qty:
				if default_bom:
					bom_doc = frappe.get_doc("BOM",default_bom)
					items = bom_doc.items
					for row in items:
						qty = float(row.qty)
						raw_rsrd_qty = product_rsrd_qty[0][0] * float(row.qty);
						data1=[]
						data1 =[[product['item_code'],product_rsrd_qty,row.item_code,row.qty,0.0, 0.0,0.0,raw_rsrd_qty,0.0]]
						qty_data = frappe.db.sql(""" select bn.warehouse,bn.item_code,bn.actual_qty,bn.ordered_qty,bn.planned_qty,
											 bn.reserved_qty,bn.projected_qty from tabBin bn where bn.item_code ='{0}'""".format(row.item_code),as_list=1,debug=1)
						for qty in qty_data:
							data1[0][4]=float(data1[0][4])+float(qty[2])   #actual_qty '''
							data1[0][5]=float(data1[0][5])+float(qty[3])   # ordered_qty"
							data1[0][6]=float(data1[0][6])+float(qty[4])   #planed_qty" 
							# data1[0][7]=float(data1[0][7])+float(qty[5])   #reserved_qty"
							data1[0][8]=float(data1[0][4])-float(data1[0][7])  #projected_qty"
							print "data1[0][8]",data1[0][8]
						print "float(data1[0][8])",float(data1[0][8]) 
						if float(data1[0][8]) < 0.0:
							data1[0][3] =concat_unit(data1[0][3],row.stock_uom)
							data1[0][4] =concat_unit(data1[0][4],row.stock_uom)
							data1[0][5] =concat_unit(data1[0][5],row.stock_uom)
							data1[0][6] =concat_unit(data1[0][6],row.stock_uom)
							data1[0][7] =concat_unit(data1[0][7],row.stock_uom)
							data1[0][8] =concat_unit(data1[0][8],row.stock_uom)
							print "-knndvmkv"	
							data.extend(data1)
							
		return data

def concat_unit(value,unit):
	return str(value)+str(unit)