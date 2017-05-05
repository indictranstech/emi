# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from erpnext.manufacturing.doctype.production_order.production_order import make_stock_entry
from emi.emi.report.item_shortage_report_with_raw_material.item_shortage_report_with_raw_material import get_data

class JobCard(Document):

	# def on_submit(self):
	# 	#self.check_pro_order()


	def validate(self):
		self.final_inspected_qty()
		f_q=qty_final(self.job_order_detail)
		print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",f_q)
		make_stock_entry(self.production_order,"Manufacture",f_q,self.name)
		self.check_pro_order()
		
	# Create Stock Entry For Final Inspection 
	def stock_entry_through_job_cart(self):
		print("hiiiiiiiiiiiiiiiiiiii ##################################### Job Card Final")
		# Stock Entry For Final Inspected Qty
		for chld in self.job_order_detail:
			if chld.process == "Final Inspection":
				po = frappe.get_doc("Production Order", chld.production_order)
				si = frappe.get_doc({
					"doctype": "Stock Entry",
					"purpose": "Material Transfer",
					"posting_date": chld.date,
					"from_warehouse": po.get('fg_warehouse'),
					"to_warehouse": "Stores - E",
					"items": get_order_items(po, chld, po.get('fg_warehouse'), "Stores - E")
				})
				si.flags.ignore_mandatory = True
				si.save(ignore_permissions=True)
				si.submit()
				frappe.db.commit()

#To Check Quantity is not Greater Than Production Order Quantity
	def final_inspected_qty(self):
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Final final_inspected_qty")
		for chld in self.job_order_detail:
			if chld.process == 'Final Inspection'  and  flt(self.quantity)<flt(chld.completed_job):
				frappe.throw("You Have Not Allowed to entered the Greater Value from Production Order Quantity")

	def check_pro_order(self):
		# po_status= frappe.db.get_value("Production Order",{"name":self.production_order},"status")
		for chld1 in self.job_order_detail:
			if chld1.process=="Final Inspection":
				self.stock_entry_through_job_cart()
		

def get_order_items(po, chld, s_warehouse, t_warehouse):
	 	# Items from Production Order
	 	items = []
	 	items.append({
			"s_warehouse": s_warehouse,
			"t_warehouse": t_warehouse,
			"item_code": po.get('production_item'),
			"qty": float(chld.completed_job),
			"uom": po.get('stock_uom'),
		})
		return items		


@frappe.whitelist()
def get_info_production(doctype, txt, searchfield, start, page_len, filters):
	#Production Order Process Filter in Job Card
	return frappe.db.sql("""select name from `tabProduction Order` where status='In Process'""",as_list=1,debug=1)

"""
get_query for Pending Sales order report
"""
@frappe.whitelist()
def sales_order_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name from `tabSales Order`
		where status = 'Draft' or status = 'To Deliver and Bill' """,as_list=1)

"""
get_query for Pending Purchase order report
"""
@frappe.whitelist()
def purchase_order_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select po.name,po.transaction_date,po.supplier
							from `tabPurchase Order` po where po.status = 'Draft' or 
							po.status = 'To Receive and Bill' """,as_list=1)
"""
get_query for item shortest report for raw material
"""
@frappe.whitelist()
def product_query(doctype, txt, searchfield, start, page_len, filters):
	data = get_shortage_product_for_raw_material()
	return data
	# return frappe.db.sql(" select bin.item_code from tabBin bin,tabItem i where bin.projected_qty <0 and i.item_code =bin.item_code and i.item_group ='Products'",as_list=1)

#added the Qty in Final Inspection Process
@frappe.whitelist()
def qty_final(job_order_detail):
	for chld in job_order_detail:
		if chld.process=='Final Inspection':
			return chld.completed_job

@frappe.whitelist()
def get_shortage_product_for_raw_material():
	shortage_product = []
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
					if float(data1[0][8]) <= 0.0:
						data.extend(data1)
						
	for row in data:
		if row[0] not in shortage_product:
			shortage_product.append(row[0])
	print "shortage_product",shortage_product
	return [[product] for product in shortage_product]
	