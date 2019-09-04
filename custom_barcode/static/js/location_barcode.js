//odoo.define('custom_barcode.LocationMenu', function (require) {
//"use strict";
//
//var core = require('web.core');
//var Model = require('web.Model');
//var Widget = require('web.Widget');
//var Dialog = require('web.Dialog');
//var Session = require('web.session');
//var BarcodeHandlerMixin = require('barcodes.BarcodeHandlerMixin');
//
//var _t = core._t;
//
//var LocationMenu = Widget.extend(BarcodeHandlerMixin, {
//    template: 'location_menu',
//
//    init: function(parent, action) {
//        // Note: BarcodeHandlerMixin.init calls this._super.init, so there's no need to do it here.
//        // Yet, "_super" must be present in a function for the class mechanism to replace it with the actual parent method.
//        this._super;
//        BarcodeHandlerMixin.init.apply(this, arguments);
//        this.message_demo_barcodes = action.params.message_demo_barcodes;
//    },
//
//    start: function() {
//        var self = this;
//        return this._super().then(function() {
//            if (self.message_demo_barcodes) {
//                self.setup_message_demo_barcodes();
//            }
//        });
//    },
//
//    on_attach_callback: function() {
//        this.start_listening();
//    },
//
//    on_detach_callback: function() {
//        this.stop_listening();
//    },
//
//    on_barcode_scanned: function(barcode) {
//        var self = this;
//        Session.rpc('/custom_barcode/scan_location', {
//            barcode: barcode,
//        }).then(function(result) {
//            if (result.action) {
//                self.do_action(result.action);
//            } else if (result.warning) {
//                self.do_warn(result.warning);
//            }
//        });
//    },
//
//});
//
//core.action_registry.add('scan_stock_lcoation_barcode', LocationMenu);
//
//return {
//	LocationMenu: LocationMenu,
//};
//
//});


odoo.define('custom_barcode.LocationMenu', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var Session = require('web.session');

var _t = core._t;

var LocationMenu = AbstractAction.extend({
    template: 'location_menu',

    init: function(parent, action) {
        // Yet, "_super" must be present in a function for the class mechanism to replace it with the actual parent method.
        this._super.apply(this, arguments);
        this.message_demo_barcodes = action.params.message_demo_barcodes;
    },

    willStart: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            return Session.user_has_group('stock.group_stock_multi_locations').then(function (has_group) {
                self.group_stock_multi_location = has_group;
            });
        });
    },

    start: function() {
        var self = this;
        core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
        return this._super().then(function() {
            if (self.message_demo_barcodes) {
                self.setup_message_demo_barcodes();
            }
        });
    },

    destroy: function () {
        core.bus.off('barcode_scanned', this, this._onBarcodeScanned);
        this._super();
    },
    
   /* setup_message_demo_barcodes: function() {
        var self = this;
        // Upon closing the message (a bootstrap alert), propose to remove it once and for all
        self.$(".message_demo_barcodes").on('close.bs.alert', function () {
            var message = _t("Do you want to permanently remove this message ?\
                It won't appear anymore, so make sure you don't need the barcodes sheet or you have a copy.");
            var options = {
                title: _t("Don't show this message again"),
                size: 'medium',
                buttons: [
                    { text: _t("Remove it"), close: true, classes: 'btn-primary', click: function() {
                        Session.rpc('/custom_barcode/scan_location');
                    }},
                    { text: _t("Leave it"), close: true }
                ],
            };
            Dialog.confirm(self, message, options);
        });
    },*/

    _onBarcodeScanned: function(barcode) {
        var self = this;
        if (!$.contains(document, this.el)) {
            return;
        }
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

core.action_registry.add('scan_stock_location_barcode', LocationMenu);

return {
	LocationMenu: LocationMenu,
};

});
