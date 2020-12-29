
odoo.define('medical_opthalmology', function (require) {
"use strict";
    var ListRenderer = require('web.ListRenderer');

       ListRenderer.include({
            _renderBody: function () {
                var $rows = this._renderRows();
                    var list_new=['medical.opthalmology','old.glass.sub','old.glass','old.glass.wizard','medical.optics']
                    console.log(this);
                    if (list_new.includes(this.__parentedParent.model)){
                        }
                    else
                        while ($rows.length < 4) {
                        $rows.push(this._renderEmptyRow());
                        }
                return $('<tbody>').append($rows);
        },

})
})