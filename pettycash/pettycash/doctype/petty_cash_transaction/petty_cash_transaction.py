# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class PettyCashTransaction(Document):
	def validate(self):
		self.validate_accounts()
		self.validate_repeating_companies()

	def validate_repeating_companies(self):
		"""Error when same company is entered multiple times in accounts"""
		accounts_list = []
		for entry in self.accounts:
			accounts_list.append(entry.company)

		if len(accounts_list) != len(set(accounts_list)):
			frappe.throw(_("Same Company is entered more than once"))

	def validate_accounts(self):
		for entry in self.accounts:
			"""Error when company of ledger account doesn't match with company selected"""
			if frappe.db.get_value("Account", entry.default_account,"Company") != entry.company:
				frappe.throw(_("Account {0} does not match with Company {1}").format(entry.default_account, entry.company))
