# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_fullname, flt, cstr, formatdate
from frappe.model.document import Document
#from erpnext.hr.utils import set_employee_name
#from erpnext.accounts.party import get_party_account
from erpnext.accounts.general_ledger import make_gl_entries
#from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from erpnext.controllers.accounts_controller import AccountsController
#from frappe.utils.csvutils import getlink

class PettyCash(AccountsController):
	def validate(self):
		self.calculate_total_amount()
		self.set_status()

	def calculate_total_amount(self):
		self.total_amount = 0
		for d in self.get('expenses'):
			self.total_amount += flt(d.amount)

	def on_submit(self):
		self.make_gl_entries()
		self.set_status()

	def on_cancel(self):
		self.make_gl_entries(cancel=True)
		self.set_status()

	def set_status(self):
		self.status = {
			"0": "Draft",
			"1": "Submitted",
			"2": "Cancelled"
		}[cstr(self.docstatus or 0)]

	def make_gl_entries(self,cancel = False):
		if flt(self.total_amount) > 0:
			gl_entries = self.get_gl_entries()
			make_gl_entries(gl_entries,cancel)

	def get_gl_entries(self):
		gl_entry = []
		total_amount = flt(self.total_amount)

		if(self.petty_cash_type == 'Cash Out'):
			#account entry
			if total_amount:
				gl_entry.append(
					self.get_gl_dict({
						"account": self.account,
						"credit": total_amount,
						"credit_in_account_currency": total_amount,
						"against": ",".join([d.default_account for d in self.expenses]),
						#"against_voucher_type": self.doctype,
						#"against_voucher": self.name,
						"remarks": 'Reference# {0} dated {1} Note: {2}'.format(self.reference_number,formatdate(self.reference_date),self.remark),
					})
				)

			#expense Entries
			for data in self.expenses:
				gl_entry.append(
					self.get_gl_dict({
						"account": data.default_account,
						"debit": data.amount,
						"debit_in_account_currency": data.amount,
						"against": self.account,
						"cost_center": self.cost_center,
						"remarks": 'Reference# {0} dated {1} Note: {2}'.format(self.reference_number,formatdate(self.reference_date),self.remark),
						"project": self.project
					})
				)
		else:
			#account entry
			if total_amount:
				gl_entry.append(
					self.get_gl_dict({
						"account": self.account,
						"debit": total_amount,
						"debit_in_account_currency": total_amount,
						"against": ",".join([d.default_account for d in self.expenses]),
						#"against_voucher_type": self.doctype,
						#"against_voucher": self.name,
						"remarks": 'Reference# {0} dated {1} Note: {2}'.format(self.reference_number,formatdate(self.reference_date),self.remark),
					})
				)

			#expense Entries
			for data in self.expenses:
				gl_entry.append(
					self.get_gl_dict({
						"account": data.default_account,
						"credit": data.amount,
						"credit_in_account_currency": data.amount,
						"against": self.account,
						"cost_center": self.cost_center,
						"remarks": 'Reference# {0} dated {1} Note: {2}'.format(self.reference_number,formatdate(self.reference_date),self.remark),
						"project": self.project
					})
				)

		return gl_entry


@frappe.whitelist()
def get_petty_cash_account(petty_cash_transaction, company):
	account = frappe.db.get_value("Petty Cash Account",
		{"parent": petty_cash_transaction, "company": company}, "default_account")

	if not account:
		frappe.throw(_("Please set default account in Expense Claim Type {0}")
			.format(petty_cash_transaction))

	return {
		"account": account
	}
