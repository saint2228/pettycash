// Copyright (c) 2018, Ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Petty Cash Transaction', {
	refresh: function(frm) {
  	frm.fields_dict["accounts"].grid.get_field("default_account").get_query = function(frm, cdt, cdn){
			var d = locals[cdt][cdn];
			return{
				filters: {
					"is_group" : 0,
					//"root_type" : "Expense",
				  'company' : d.company
				}
			}
		}
	}
});
