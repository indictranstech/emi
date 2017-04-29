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
			   ("Product") + ":Data:100",
			   ("Warehouse") + ":Data:100",
			   ("Qty To Produce") + ":Data:160",
			   ("Item Code") + ":Data:100",
			   ("Qty For Per Product") +":Data:130",
			   ("Actual Qty") + ":Data:100",
			   ("Ordered Qty") + ":Data:100",
			   ("Planned Qty") + ":Data:100",
			   ("Reserved Qty") + ":Data:100",
			   ("Projected Qty") + ":Data:100",
 
			 ]

	return columns
def get_data(filters):
	if filters:
		print "\n\n\n-------------"
		data=[];
		product_rsrd_qty =0.0;
		raw_rsrd_qty = 0.0;
		default_bom = frappe.db.get_value("Item",{'item_code':filters.item_code},"default_bom")
		print "default_bom",default_bom
		product_rsrd_qty = frappe.db.sql("""select reserved_qty from tabBin where item_code ='{0}'""".format(filters.item_code),as_list=1)
		print "product_rsrd_qty",product_rsrd_qty[0][0]
		if default_bom:
			bom_doc = frappe.get_doc("BOM",default_bom)
			items = bom_doc.items
			for row in items:
				print "row.qty",row.qty
				print "row.item_code",row.item_code
				print "row.unit",row.stock_uom
				qty = float(row.qty)
				raw_rsrd_qty = product_rsrd_qty[0][0] * float(row.qty);
				data1=[]
				data1 =frappe.db.sql("""select bom.item,bn.warehouse,b1.reserved_qty,bn.item_code,bi.qty,
										bn.actual_qty,bn.ordered_qty,bn.planned_qty,bn.reserved_qty,bn.projected_qty 
											from tabBOM bom,`tabBOM Item`bi,tabBin bn,tabBin b1   
										where bi.parent = bom.name and bom.name = '{0}' and bi.item_code='{1}' 
										and bn.item_code ='{1}' and b1.item_code=bom.item""".format(default_bom,row.item_code),as_list=1,debug=1)
					
				if data1:
					print "data1",data1
					print "data1",data1[0][6]
					data1[0][8] = raw_rsrd_qty  
					data1[0][9] = data1[0][5] -data1[0][8]
					data1[0][4] = concat_unit(data1[0][4],row.stock_uom)
					data1[0][5]	= concat_unit(data1[0][5],row.stock_uom)
					data1[0][6] = concat_unit(data1[0][6],row.stock_uom)
					data1[0][7] = concat_unit(data1[0][7],row.stock_uom)
					data1[0][8] = concat_unit(data1[0][8],row.stock_uom)
					data1[0][9] = concat_unit(data1[0][9],row.stock_uom)
					
					data.extend(data1)
		print "\n\n\n-------------"
		return data	
	else:
		products = frappe.db.sql("select item_code from tabItem where item_group ='Products'",as_dict=1)
		data =[]
		print "\n\n\nWithout Filter"
		product_rsrd_qty =0.0;
		raw_rsrd_qty = 0.0;
		for product in products:
			print "product",product
			default_bom = frappe.db.get_value("Item",{'item_code':product['item_code']},"default_bom")
			print "default_bom",default_bom
			product_rsrd_qty = frappe.db.sql("""select reserved_qty from tabBin where item_code ='{0}'""".format(product['item_code']),as_list=1)
			if product_rsrd_qty:
				print "product_rsrd_qty",product_rsrd_qty[0][0]
				if default_bom:
					bom_doc = frappe.get_doc("BOM",default_bom)
					items = bom_doc.items
					for row in items:
						print "row.qty",row.qty
						print "row.item_code",row.item_code
						print "row.unit",row.stock_uom
						qty = float(row.qty)
						raw_rsrd_qty = product_rsrd_qty[0][0] * float(row.qty);
						data1=[]
						data1 =frappe.db.sql("""select bom.item,bn.warehouse,b1.reserved_qty,bn.item_code,bi.qty,
												bn.actual_qty,bn.ordered_qty,bn.planned_qty,bn.reserved_qty,bn.projected_qty 
												from tabBOM bom,`tabBOM Item`bi,tabBin bn,tabBin b1   
												where bi.parent = bom.name and bom.name = '{0}' and bi.item_code='{1}' 
												and bn.item_code ='{1}' and b1.item_code=bom.item""".format(default_bom,row.item_code),as_list=1,debug=1)

						if data1:
							print "data1",data1
							print "data1",data1[0][6]
							data1[0][8] = raw_rsrd_qty  
							data1[0][9] = data1[0][5] -data1[0][8]
							data1[0][4] = concat_unit(data1[0][4],row.stock_uom)
							data1[0][5]	= concat_unit(data1[0][5],row.stock_uom)
							data1[0][6] = concat_unit(data1[0][6],row.stock_uom)
							data1[0][7] = concat_unit(data1[0][7],row.stock_uom)
							data1[0][8] = concat_unit(data1[0][8],row.stock_uom)
							data1[0][9] = concat_unit(data1[0][9],row.stock_uom)
							
							data.extend(data1)


		# for item in item_code:
		# 	default_bom = frappe.db.get_value("Item",{'item_code':item['item_code']},"default_bom")
		# 	if default_bom:
		# 		raw_items = frappe.db.sql("select item_code from `tabBOM Item` where parent ='{0}'".format(default_bom),as_list=1)
		# 		for raw in raw_items:
		# 			data1=[]
		# 			data1 =frappe.db.sql("select b.item,warehouse,item_code,actual_qty,ordered_qty,planned_qty,reserved_qty,projected_qty from tabBin,tabBOM b where item_code ='{0}' and b.name='{1}' ".format(raw[0],default_bom),as_list=1,debug=1)
		# 			data.extend(data1)
		# return data
		print "data",data
		print "\n\n\n"
		return data

def concat_unit(value,unit):
	return str(value)+str(unit)