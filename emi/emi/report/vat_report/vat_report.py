# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe.utils import flt, getdate, cstr
from frappe import _
from erpnext.accounts.utils import get_account_currency

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


def execute(filters=None):
	data = []
	account_details = {}
	for acc in frappe.db.sql("""select name, is_group from tabAccount where parent_account = 'Duties and Taxes - E'""", as_dict=1):
		account_details.setdefault(acc.name, acc)
	validate_filters(filters, account_details)

	validate_party(filters)

	filters = set_account_currency(filters)
	columns = get_columns(filters)
	res = get_result(filters, account_details)
	# print"++++++++++++++++++",res
	'''
	  Adding trn and territory 
	'''
	for row in res:
		trn = territory =''
		part1 = row[0:9]
		if row[7] and row[8]:
			trn = frappe.db.get_value(row[7],{"name":row[8]},"tax_registration_no")
			territory = frappe.db.get_value(row[7],{"name":row[8]},"territory")
			part1.append(trn)
			part1.append(territory)
		else:
			part1.append(territory)
		
		part2  =row[9:len(row)]
		part1.extend(part2)
		data.append(part1)	
	vat_data = get_vat_data(filters)
	if vat_data:
		data.append(['',vat_data])
	return columns, data,vat_data

def validate_filters(filters, account_details):
	if not filters.get('company'):
		frappe.throw(_('{0} is mandatory').format(_('Company')))

	if filters.get("account") and not account_details.get(filters.account):
		frappe.throw(_("Account {0} does not exists").format(filters.account))

	if filters.get("account") and filters.get("group_by_account") \
			and account_details[filters.account].is_group == 0:
		frappe.throw(_("Can not filter based on Account, if grouped by Account"))

	if filters.get("voucher_no") and filters.get("group_by_voucher"):
		frappe.throw(_("Can not filter based on Voucher No, if grouped by Voucher"))

	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date must be before To Date"))


def validate_party(filters):
	party_type, party = filters.get("party_type"), filters.get("party")

	if party:
		if not party_type:
			frappe.throw(_("To filter based on Party, select Party Type first"))
		elif not frappe.db.exists(party_type, party):
			frappe.throw(_("Invalid {0}: {1}").format(party_type, party))

def set_account_currency(filters):
	if not (filters.get("account") or filters.get("party")):
		return filters
	else:
		filters["company_currency"] = frappe.db.get_value("Company", filters.company, "default_currency")
		account_currency = None

		if filters.get("account"):
			account_currency = get_account_currency(filters.account)
		elif filters.get("party"):
			gle_currency = frappe.db.get_value("GL Entry", {"party_type": filters.party_type,
				"party": filters.party, "company": filters.company}, "account_currency")
			if gle_currency:
				account_currency = gle_currency
			else:
				account_currency = frappe.db.get_value(filters.party_type, filters.party, "default_currency")

		filters["account_currency"] = account_currency or filters.company_currency

		if filters.account_currency != filters.company_currency:
			filters["show_in_account_currency"] = 1

		return filters

def get_columns(filters):
	columns = [
		_("Posting Date") + ":Date:90", _("Account") + ":Link/Account:200",
		_("Debit") + ":Float:100", _("Credit") + ":Float:100"
	]

	if filters.get("show_in_account_currency"):
		columns += [
			_("Debit") + " (" + filters.account_currency + ")" + ":Float:100",
			_("Credit") + " (" + filters.account_currency + ")" + ":Float:100"
		]

	columns += [
		_("Voucher Type") + "::120", _("Voucher No") + ":Dynamic Link/"+_("Voucher Type")+":160",
		_("Against Account") + "::120", _("Party Type") + "::80", _("Party") + "::150", _("TRN") + "::150", _("Territory") + "::150",
		_("Project") + ":Link/Project:100", _("Cost Center") + ":Link/Cost Center:100",
		_("Against Voucher Type") + "::120", _("Against Voucher") + ":Dynamic Link/"+_("Against Voucher Type")+":160",
		_("Remarks") + "::400"
	]

	return columns

def get_result(filters, account_details):
	gl_entries = get_gl_entries(filters,account_details)

	data = get_data_with_opening_closing(filters, account_details, gl_entries)

	result = get_result_as_list(data, filters)

	return result

def get_gl_entries(filters,account_details):

	if filters.get('account'):
		select_fields = """, sum(debit_in_account_currency) as debit_in_account_currency,
		sum(credit_in_account_currency) as credit_in_account_currency""" \
		if filters.get("show_in_account_currency") else ""

		group_by_condition = "group by voucher_type, voucher_no, account, cost_center" \
			if filters.get("group_by_voucher") else "group by name"

		gl_entries = frappe.db.sql("""
			select
				posting_date, account, party_type, party,
				sum(debit) as debit, sum(credit) as credit,
				voucher_type, voucher_no, cost_center, project,
				against_voucher_type, against_voucher,
				remarks, against, is_opening {select_fields}
			from `tabGL Entry`
			where company=%(company)s {conditions}
			{group_by_condition}
			order by posting_date, account"""\
			.format(select_fields=select_fields, conditions=get_conditions(filters),
				group_by_condition=group_by_condition), filters, as_dict=1)
		return gl_entries
	else:
		company = from_date =''
		accounts = []
		for key in filters:
			if key =='company':
				company =filters.get(key)
			if key == 'from_date':
				from_date = filters.get(key)
		# if account_details:		
		# 	for row in dict(account_details):
		# 		accounts.append(str(row))
		account = ('RCM VAT - E','Output VAT  - E','Input Vat - E','VAT 5% - E')
		accounts = tuple( acc.encode('UTF8') for acc in account if acc)
		conditions = "and posting_date >= {0} and account in {1}".format(from_date,accounts)
		
		select_fields = """, sum(debit_in_account_currency) as debit_in_account_currency,
		sum(credit_in_account_currency) as credit_in_account_currency""" \
		if filters.get("show_in_account_currency") else ""

		group_by_condition = "group by voucher_type, voucher_no, account, cost_center" \
			if filters.get("group_by_voucher") else "group by name"
		
		gl_entries = frappe.db.sql("""
			select
				posting_date, account, party_type, party,
				sum(debit) as debit, sum(credit) as credit,
				voucher_type, voucher_no, cost_center, project,
				against_voucher_type, against_voucher,
				remarks, against, is_opening {select_fields}
			from `tabGL Entry`
			where company= '{company}'{conditions}
			{group_by_condition}
			order by posting_date, account"""\
			.format(select_fields=select_fields,company=company,conditions=str(conditions),
				group_by_condition=group_by_condition), as_dict=1)
		return gl_entries

def get_conditions(filters):
	conditions = []
	if filters.get("account"):
		lft, rgt = frappe.db.get_value("Account", filters["account"], ["lft", "rgt"])
		conditions.append("""account in (select name from tabAccount
			where lft>=%s and rgt<=%s and docstatus<2)""" % (lft, rgt))

	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")

	if filters.get("party_type"):
		conditions.append("party_type=%(party_type)s")

	if filters.get("party"):
		conditions.append("party=%(party)s")

	if not (filters.get("account") or filters.get("party") or filters.get("group_by_account")):
		conditions.append("posting_date >=%(from_date)s")

	from frappe.desk.reportview import build_match_conditions
	match_conditions = build_match_conditions("GL Entry")
	if match_conditions: conditions.append(match_conditions)

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_data_with_opening_closing(filters, account_details, gl_entries):
	data = []
	gle_map = initialize_gle_map(gl_entries)

	opening, total_debit, total_credit, opening_in_account_currency, total_debit_in_account_currency, \
		total_credit_in_account_currency, gle_map = get_accountwise_gle(filters, gl_entries, gle_map)

	# Opening for filtered account
	if filters.get("account") or filters.get("party"):
		data += [get_balance_row(_("Opening"), opening, opening_in_account_currency), {}]

	if filters.get("group_by_account"):
		for acc, acc_dict in gle_map.items():
			if acc_dict.entries:
				# Opening for individual ledger, if grouped by account
				data.append(get_balance_row(_("Opening"), acc_dict.opening,
					acc_dict.opening_in_account_currency))

				data += acc_dict.entries

				# Totals and closing for individual ledger, if grouped by account
				account_closing = acc_dict.opening + acc_dict.total_debit - acc_dict.total_credit
				account_closing_in_account_currency = acc_dict.opening_in_account_currency \
					+ acc_dict.total_debit_in_account_currency - acc_dict.total_credit_in_account_currency

				data += [{"account": "'" + _("Totals") + "'", "debit": acc_dict.total_debit,
					"credit": acc_dict.total_credit},
					get_balance_row(_("Closing (Opening + Totals)"),
						account_closing, account_closing_in_account_currency), {}]

	else:
		for gl in gl_entries:
			if gl.posting_date >= getdate(filters.from_date) and gl.posting_date <= getdate(filters.to_date) \
					and gl.is_opening == "No":
				data.append(gl)


	# Total debit and credit between from and to date
	if total_debit or total_credit:
		data.append({
			"account": "'" + _("Totals") + "'",
			"debit": total_debit,
			"credit": total_credit,
			"debit_in_account_currency": total_debit_in_account_currency,
			"credit_in_account_currency": total_credit_in_account_currency
		})

	# Closing for filtered account
	if filters.get("account") or filters.get("party"):
		closing = opening + total_debit - total_credit
		closing_in_account_currency = opening_in_account_currency + \
			total_debit_in_account_currency - total_credit_in_account_currency

		data.append(get_balance_row(_("Closing (Opening + Totals)"),
			closing, closing_in_account_currency))

	return data

def initialize_gle_map(gl_entries):
	gle_map = frappe._dict()
	for gle in gl_entries:
		gle_map.setdefault(gle.account, frappe._dict({
			"opening": 0,
			"opening_in_account_currency": 0,
			"entries": [],
			"total_debit": 0,
			"total_debit_in_account_currency": 0,
			"total_credit": 0,
			"total_credit_in_account_currency": 0,
			"closing": 0,
			"closing_in_account_currency": 0
		}))
	return gle_map

def get_accountwise_gle(filters, gl_entries, gle_map):
	opening, total_debit, total_credit = 0, 0, 0
	opening_in_account_currency, total_debit_in_account_currency, total_credit_in_account_currency = 0, 0, 0

	from_date, to_date = getdate(filters.from_date), getdate(filters.to_date)
	for gle in gl_entries:
		amount = flt(gle.debit, 3) - flt(gle.credit, 3)
		amount_in_account_currency = flt(gle.debit_in_account_currency, 3) - flt(gle.credit_in_account_currency, 3)

		if (filters.get("account") or filters.get("party") or filters.get("group_by_account")) \
				and (gle.posting_date < from_date or cstr(gle.is_opening) == "Yes"):

			gle_map[gle.account].opening += amount
			if filters.get("show_in_account_currency"):
				gle_map[gle.account].opening_in_account_currency += amount_in_account_currency

			if filters.get("account") or filters.get("party"):
				opening += amount
				if filters.get("show_in_account_currency"):
					opening_in_account_currency += amount_in_account_currency

		elif gle.posting_date <= to_date:
			gle_map[gle.account].entries.append(gle)
			gle_map[gle.account].total_debit += flt(gle.debit, 3)
			gle_map[gle.account].total_credit += flt(gle.credit, 3)

			total_debit += flt(gle.debit, 3)
			total_credit += flt(gle.credit, 3)

			if filters.get("show_in_account_currency"):
				gle_map[gle.account].total_debit_in_account_currency += flt(gle.debit_in_account_currency, 3)
				gle_map[gle.account].total_credit_in_account_currency += flt(gle.credit_in_account_currency, 3)

				total_debit_in_account_currency += flt(gle.debit_in_account_currency, 3)
				total_credit_in_account_currency += flt(gle.credit_in_account_currency, 3)

	return opening, total_debit, total_credit, opening_in_account_currency, \
		total_debit_in_account_currency, total_credit_in_account_currency, gle_map

def get_balance_row(label, balance, balance_in_account_currency=None):
	balance_row = {
		"account": "'" + label + "'",
		"debit": balance if balance > 0 else 0,
		"credit": -1*balance if balance < 0 else 0
	}

	if balance_in_account_currency != None:
		balance_row.update({
			"debit_in_account_currency": balance_in_account_currency if balance_in_account_currency > 0 else 0,
			"credit_in_account_currency": -1*balance_in_account_currency if balance_in_account_currency < 0 else 0
		})

	return balance_row

def get_result_as_list(data, filters):
	result = []
	for d in data:
		row = [d.get("posting_date"), d.get("account"), d.get("debit"), d.get("credit")]

		if filters.get("show_in_account_currency"):
			row += [d.get("debit_in_account_currency"), d.get("credit_in_account_currency")]

		row += [d.get("voucher_type"), d.get("voucher_no"), d.get("against"),
			d.get("party_type"), d.get("party"), d.get("project"), d.get("cost_center"), d.get("against_voucher_type"), d.get("against_voucher"), d.get("remarks")
		]

		result.append(row)

	return result

def get_vat_data(filters=None):
	account_details = {}
	total_input_vat = total_output_vat = total_rcm_vat = 0.0
	for acc in frappe.db.sql("""select name, is_group from tabAccount""", as_dict=1):
		account_details.setdefault(acc.name, acc)
	'''Input VAT'''
	filters['account'] ='Input Vat - E'
	validate_filters(filters, account_details)
	validate_party(filters)
	filters = set_account_currency(filters)
	input_vat_data = get_result(filters, account_details)
	for row in input_vat_data:
		if row[1] == "'Closing (Opening + Totals)'":
			total_input_vat = row[3]
			
	'''Output VAT'''
	filters['account'] ='Output VAT  - E'
	validate_filters(filters, account_details)
	validate_party(filters)
	filters = set_account_currency(filters)
	output_vat_data = get_result(filters, account_details)
	for row in output_vat_data:
		if row[1] == "'Closing (Opening + Totals)'":
			total_output_vat = row[3]

	'''RCM VAT'''
	filters['account'] ='RCM VAT - E'
	validate_filters(filters, account_details)
	validate_party(filters)
	filters = set_account_currency(filters)
	rcm_vat_data = get_result(filters, account_details)
	for row in rcm_vat_data:
		if row[1] == "'Closing (Opening + Totals)'":
			total_rcm_vat = row[2]
	
	total_vat_payble = total_output_vat + total_rcm_vat
	net_vat_payable = total_output_vat - total_input_vat
	vat_calculation_table = frappe.render_template("templates/vat_report/vat_calculation.html", {"total_input_vat":total_input_vat,"total_output_vat":total_output_vat,"total_rcm_vat":total_rcm_vat,"total_vat_payble":total_vat_payble,"net_vat_payable":net_vat_payable}),
	return vat_calculation_table
