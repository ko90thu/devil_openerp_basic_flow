from openerp import SUPERUSER_ID
from openerp import pooler
from openerp.osv import fields, osv
from osv import osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class devil_formulas(osv.osv):        
    
    def _amount_all(self, cr, uid, ids, total, arg, context=None):       
        val={}        
        for total in self.browse(cr,uid,ids,context=None):
            if total['total_amt_disc'] or total['total_amt_disc'] != 0:
                val[total.id]={'total_amount': 0.0,}
                val1=0
                for line in total.formula_line:
                    val1+=line['price_subtotal'] 
                val[total.id]=val1-total['total_amt_disc']
            else:
                val[total.id]={'total_amount': 0.0,}
                val1=0
                for line in total.formula_line:
                    val1+=line['price_subtotal'] 
                val[total.id]=val1
        return val
    
    STATE_SELECTION = [
        ('draft', 'New'),    
        ('open', 'Accepted'),
        ('cancel', 'Refused'),
        ('close', 'Done')
    ]
            
    _name='devil.formulas'
    _description='Formula Calculation'
    _columns={
              'name': fields.char('Transaction Code',size=124),
              'date': fields.date('Transaction Date'),
              'cust_id': fields.many2one('devil.customer','Customer'),
              'formula_line': fields.one2many('devil.items.lines','formula_id','FormulaLines'),
              'total_amt_disc': fields.float('Amount Discount', required=True, ),
              'total_amount': fields.function(_amount_all, string='TotalAmount'),
              'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, select=True),
    }
    _defaults = {
        'state': lambda *a: 'draft',
    }
    
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
    
    def devil_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def devil_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def devil_close(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def devil_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    
devil_formulas()


class devil_items_lines(osv.osv):
    
    def _amount_line(self, cr, uid, ids, sub, arg, context=None):        
        val={}        
        obj_line=self.pool.get('devil.items.lines')       
        for test in self.browse(cr,uid,ids,context=context):
            if test['item_qty'] >= test['item_name']['qty']:
                #raise osv.except_osv(_('Warning!'), _('Not Enough Qty.')) 
                val[test.id]=0.0
            else:           
                val[test.id]=test['item_qty']*test['price_unit']
        return val        
         
   
                   
    _name='devil.items.lines'
    _description='Devil Items Lines'
    _columns={
              'name': fields.char('Description',size=124,help='Something about items'),
              'item_qty': fields.integer('Item Qty'),
              'item_name':fields.many2one('devil.items','Item',size=124),
              'price_unit': fields.float('Unit Price', required=True, ),
              'price_subtotal': fields.function(_amount_line, string='Subtotal'),
              'formula_id': fields.many2one('devil.formulas','Formula Reference',select=True,required=True,ondelete='cascade'),
              
            
    }    
  
        
        
devil_items_lines()



class devil_items(osv.osv):
    _name='devil.items'
    _description='Devil Items'
    _columns={
              'name': fields.char('Items Name',size=124,help='Sub Items'),
              'qty': fields.integer('Qty'),              
    }
devil_items()

class devil_customer(osv.osv):
    _name='devil.customer'
    _description='Devil Customer'
    _columns={
              'name': fields.char('Customer Name',size=25),
              'ref': fields.char('Code',size=12),
              'nrc': fields.char('NRC',size=18),
              'mobile': fields.integer('Mobile'),
              'address': fields.char('Address',size=124),
    }
devil_customer()



