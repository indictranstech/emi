frappe.pages['dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Production Order Dashboard',
		single_column: true
	});
		wrapper.asset_dashboard = new asset_dashboard(wrapper)
	frappe.breadcrumbs.add("Production Order");
}


frappe.pages['dashboard'].refresh = function(wrapper) {
	wrapper.asset_dashboard;
}



asset_dashboard = Class.extend({
	init: function(wrapper) {
		var me = this;
		this.wrapper_page = wrapper.page;
		this.page = $(wrapper).find('.layout-main-section');
		this.wrapper = $(wrapper).find('.page-content');
		this.set_fields();
		if(!frappe.route_options) {
			me.get_column_data();
		}
	},
	set_fields:function(){
		var me = this;

			

		html = "<div class='row' style='padding: 50px;'>\
				<div class='col-xs-12 pie-chart'></div>\
				</div>"
		me.page.html(html)

		
		
	},
	
	refresh: function() {
		console.log("refresh")
		var me = this;
		me.get_column_data();

	},	
	get_column_data:function(){
		var me =this;
		console.log("get_column_data in");
		frappe.call({
			method: "emi.emi.page.dashboard.dashboard.get_data",
			
			args: {
				"from_date":"",
				"to_date":""
			},
			callback: function(r) {
				if (r.message){
					console.log(r.message,"dddadtaaaa")
					me.data = r.message;
					var __html = frappe.render_template("dashboard",{"data":r.message})
					$(me.page).find(".pie-chart").empty();
					me.page.find(".pie-chart").append(__html)
					me.set_chart();
				}
			}
		})		
	},
	set_chart: function(){
		var me = this;
		console.log("In chart with data",me.data);
		console.log($("#assets_condition"))
		var chart = c3.generate({
			bindto:'#assets_condition',
			data: {

			    columns: [
			        ['data1', 30, 200, 100, 400, 150, 250],
			        ['data2', 130, 100, 140, 200, 150, 50]
			    ],
			    type: 'bar'
			},
			bar: {
			    width: {
			        ratio: 0.5 // this makes bar width 50% of length between ticks
			    }
			}
		});

		/*chart for Asset Register */
		/*var chart1 = c3.generate({

	        bindto:'#assets_condition',
	        data: {
				columns: [
					[__("Working"), me.data["working"]["count"] ? me.data["working"]["count"]: 0],
					[__("Non Working"), me.data["non_workinng"]["count"] ? me.data["non_workinng"]["count"]:0],
					[__("Under maintenance"), me.data["under_maintenance"]["count"] ? me.data["under_maintenance"]["count"]:0],
					[__("Retired"), me.data["retired"]["count"] ? me.data["retired"]["count"]:0]
				],
				type : 'pie',
				onclick: function (d, i) { console.log("onclick",d,i);

					// frappe.set_route("List", "Asset Register", {'status': "Working"});
					/*frappe.set_route("List", "Asset Register");

				 },
				labels: true
			},
			pie: {
				label: {
					format: function(value, ratio, id) {
						return value;
					}
				}
			},	
      	});
*/

	}
})