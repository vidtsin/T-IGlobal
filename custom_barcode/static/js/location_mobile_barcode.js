odoo.define('custom_barcode.mobile_barcode', function (require) {
"use strict";

var LocatioMainMenu = require('custom_barcode.LocationMenu').LocationMenu;
var mobile = require('web_mobile.rpc');

LocatioMainMenu.include({
    events: _.defaults({
        'click .o_stock_mobile_barcode': 'open_mobile_scanner'
    }, LocatioMainMenu.prototype.events),
    start: function(){
        if(!mobile.methods.scanBarcode){
            this.$el.find(".o_stock_mobile_barcode").remove();
        }
        return this._super.apply(this, arguments);
        
    },
    open_mobile_scanner: function(){
        var self = this;
        mobile.methods.scanBarcode().then(function(response){
            var barcode = response.data;
            if(barcode){
                self.on_barcode_scanned(barcode);
                mobile.methods.vibrate({'duration': 100});
            }else{
                mobile.methods.showToast({'message':'Please, Scan again !!'});
            }
        });
    }
});


});
