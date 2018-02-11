frappe.listview_settings['Petty Cash'] = {
	//add_fields: ["petty_cash_type", "posting_date", "employee_name", "company"],
  add_fields: ["petty_cash_type"],
  get_indicator: function(doc) {
		if(doc.docstatus==0) {
			return [__("Draft", "red", "docstatus,=,0")]
		} else if(doc.docstatus==2) {
			return [__("Cancelled", "grey", "docstatus,=,2")]
		} else {
			return [__(doc.petty_cash_type), "blue", "petty_cash_type,=," + doc.petty_cash_type]
		}
	}
};


/*
frappe.listview_settings['Petty Cash'] = {
	filters:[["docstatus","!=","1"]]
};
*/
