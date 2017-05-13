# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint
from emi.emi.custom_methods import make_stock_entry
from emi.emi.report.item_shortage_report_with_raw_material.item_shortage_report_with_raw_material import get_data
from collections import defaultdict, OrderedDict


class JobCard(Document):

	def validate(self):
		self.validate_final_inspected_qty()
	
	def validate_final_inspected_qty(self):
		#To Check Quantity is not Greater Than Production Order quantity
		for chld in self.job_order_detail:
			if chld.process == 'Final Inspection' and flt(self.quantity) < flt(chld.completed_job):
				frappe.throw("You Have Not Allowed to entered the Greater Value from Production Order Quantity")


	def on_submit(self):
		abbr = self.validate_for_default_company()
		self.init_inspection_processes(abbr)

	
	def validate_for_default_company(self):
		company = frappe.db.get_value("Global Defaults", None, "default_company")
		if not company:
			frappe.throw(_("Please set default company in Global Defaults."))
		return frappe.db.get_value("Company", company, "abbr")


	def init_inspection_processes(self, abbr):
		galvanize_dict, final_insp_dict = self.get_process_wise_dict()
		final_insp_warehouse = "Factory Store Polish - " + abbr
		
		# Initiate Pre-galvanize inspection (Manufacture) process.
		for prod_order, manuf_qty in galvanize_dict.iteritems():
			if isinstance(prod_order, unicode) and manuf_qty:
				black_qty = galvanize_dict.get(tuple([prod_order, "black_qty"]), 0)
				self.init_stock_entry_for_pre_galvanize(prod_order, manuf_qty, black_qty, abbr)
		
		# Initaie Final Inspection (material Transfer to Stores) process.		
		for prod_order, qty in final_insp_dict.iteritems():
			if qty:
				frm_warehouse = prod_order[1] or final_insp_warehouse
				self.init_stock_entry_for_final_inspection(prod_order[0], frm_warehouse, qty, abbr)

	
	def get_process_wise_dict(self):
		""" According to production order,Get Pre-galvanize process dict 
			containing black & non-black qty & Final-Inspection dict """

		galvanize_dict = defaultdict(float)
		final_insp_dict = defaultdict(float)

		for row in self.job_order_detail:
			if row.process == "Pre Gal Insp":
				galvanize_dict[row.production_order] += flt(row.completed_job)
				if row.black_material == "Yes":
					galvanize_dict[tuple([row.production_order, "black_qty"])] += flt(row.completed_job)
				else:
					galvanize_dict[tuple([row.production_order, "non_black_qty"])] += flt(row.completed_job)
			if row.process == "Final Inspection":
				final_insp_dict[tuple([row.production_order, row.inspection_warehouse])] += flt(row.completed_job)
		return galvanize_dict, final_insp_dict


	def init_stock_entry_for_pre_galvanize(self, prod_order, manuf_qty, black_qty, abbr):
		"""Make Manufacture stock entry according to qty & 
			make material transfer entry if black material exists"""
	
		po_doc = make_stock_entry(prod_order, "Manufacture", manuf_qty, via_job_card=True)
		black_warehouse = "Factory Store Black - " + abbr
		if black_qty:
			self.make_stock_entry(po_doc, black_warehouse, black_qty)
	

	def init_stock_entry_for_final_inspection(self, po, frm_warehouse, qty, abbr):
		"Final inspection stock entry (Material Transfer)"
		po_doc = frappe.get_doc("Production Order", po)
		self.make_stock_entry(po_doc, "Stores - " + abbr, qty, frm_warehouse)
		
	
	def make_stock_entry(self, po, tg_warehouse, qty, frm_warehouse=None):
		"Make material transfer stock entry"
		doc = frappe.get_doc({
			"doctype":"Stock Entry",
			"purpose":"Material Transfer",
			"company":po.company,
			"from_warehouse": frm_warehouse or po.get('fg_warehouse'),
			"to_warehouse": tg_warehouse,
			"items": self.get_se_items(po, qty, frm_warehouse or po.get('fg_warehouse'), tg_warehouse)
		})
		doc.save(ignore_permissions=True)
		doc.submit()
		

	def get_se_items(self, po, qty, s_warehouse, t_warehouse):
		# Items from Production Order
		items = []
		items.append({
			"s_warehouse":s_warehouse,
			"t_warehouse":t_warehouse,
			"item_code":po.get('production_item'),
			"item_name":po.get("production_item"),
			"description":po.get("description"),
			"qty":qty,
			"uom":po.get('stock_uom')
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
	