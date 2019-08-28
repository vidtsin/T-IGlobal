odoo.define('custom_barcode.LocationMenu', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.Model');
var Widget = require('web.Widget');
var Dialog = require('web.Dialog');
var Session = require('web.session');
var BarcodeHandlerMixin = require('barcodes.BarcodeHandlerMixin');

var _t = core._t;

var LocationMenu = Widget.extend(BarcodeHandlerMixin, {
    template: 'location_menu',

    init: function(parent, action) {
        // Note: BarcodeHandlerMixin.init calls this._super.init, so there's no need to do it here.
        // Yet, "_super" must be present in a function for the class mechanism to replace it with the actual parent method.
        this._super;
        BarcodeHandlerMixin.init.apply(this, arguments);
        this.message_demo_barcodes = action.params.message_demo_barcodes;
    },

    start: function() {
        var self = this;
        return this._super().then(function() {
            if (self.message_demo_barcodes) {
                self.setup_message_demo_barcodes();
            }
        });
    },

    on_attach_callback: function() {
        this.start_listening();
    },

    on_detach_callback: function() {
        this.stop_listening();
    },

    on_barcode_scanned: function(barcode) {
        var self = this;
        Session.rpc('/custom_barcode/scan_location', {
            barcode: barcode,
        }).then(function(result) {
            if (result.action) {
                self.do_action(result.action);
            } else if (result.warning) {
                self.do_warn(result.warning);
            }
        });
    },

});

core.action_registry.add('scan_stock_lcoation_barcode', LocationMenu);

return {
	LocationMenu: LocationMenu,
};

});
