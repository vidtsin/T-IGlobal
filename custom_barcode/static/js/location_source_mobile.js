odoo.define('custom_barcode.source_mobile_barcode', function (require) {
"use strict";

var LocationView = require('custom_barcode.LocationView').LocationView;
var mobile = require('web_mobile.rpc');

LocationView.include({
    events: _.defaults({
        'click .o_stock_mobile_barcode': 'open_mobile_scanner'
    }, LocationView.prototype.events),
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
