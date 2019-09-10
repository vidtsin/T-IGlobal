# -*- coding: utf-8 -*-
{
  "name"                 :  "MRP Requisition",
  "summary"              :  "Material requisition",
  "category"             :  "Manufacturing",
  "version"              :  "1.3",
  "sequence"             :  1,
"author"               :  "PPTS [India] Pvt.Ltd.",
"website"              :  "https://www.pptssolutions.com",
  "description"          :  """
        To Raise the Material Request from MRP
""",
  "depends"              :  [
                             'stock','mrp'
                            ],
  "data"                 :  [
                            'data/ir_sequence_data.xml',
                            'security/ir.model.access.csv',
                            'views/department.xml',
                            'views/mrp_requisition.xml',
                            'views/stock_move_views.xml',
                            'views/stock_picking_views.xml',
                            'views/mrp_production_views.xml'
                          
                            ],
#   "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}