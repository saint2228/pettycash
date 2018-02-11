// Copyright (c) 2018, Ridhosribumi and contributors
// For license information, please see license.txt

frappe.provide("pettycash.pettycash");

pettycash.pettycash.PettyCashController = frappe.ui.form.Controller.extend({
	petty_type: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(!doc.company) {
			d.petty_type = "";
			frappe.msgprint(__("Please set the Company"));
			this.frm.refresh_fields();
			return;
		}

		if(!d.petty_type) {
			return;
		}

		return frappe.call({
			method: "pettycash.pettycash.doctype.petty_cash.petty_cash.get_petty_cash_account",
			args: {
				"petty_cash_transaction": d.petty_type,
				"company": doc.company
			},
			callback: function(r) {
				if (r.message) {
					d.default_account = r.message.account;
				}
			}
		});
	}
});

$.extend(cur_frm.cscript, new pettycash.pettycash.PettyCashController({frm: cur_frm}));

frappe.ui.form.on('Petty Cash', {
	setup: function(frm){
		frm.trigger("set_query_for_cost_center");
		frm.trigger("set_query_for_account")
		frm.add_fetch("company", "cost_center", "cost_center");
		frm.add_fetch("company", "default_cash_account", "account");
	},

	refresh: function(frm) {
		frm.trigger("toggle_fields");

		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__('Accounting Ledger'), function() {
				frappe.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: frm.doc.posting_date,
					company: frm.doc.company,
					group_by_voucher: false
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	},

	set_query_for_cost_center: function(frm){
		frm.fields_dict["cost_center"].get_query = function(){
			return{
				filters: {
					"company": frm.doc.company
				}
			}
		}
	},

	set_query_for_account: function(frm) {
		frm.fields_dict["account"].get_query = function() {
			return {
				filters: {
					"report_type": "Balance Sheet",
					"account_type": "Cash",
					"is_group":0
				}
			};
		};
	},
});

cur_frm.cscript.validate = function(doc) {
	cur_frm.cscript.calculate_total(doc);
};

cur_frm.cscript.calculate_total = function(doc){
	doc.total_amount = 0;
	$.each((doc.expenses || []), function(i, d) {
		doc.total_amount += d.amount;

	});

	refresh_field("total_amount");
};

cur_frm.cscript.calculate_total_amount = function(doc,cdt,cdn){
	cur_frm.cscript.calculate_total(doc,cdt,cdn);
};
