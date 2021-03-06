# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import UserError

import base64


class P24AccountJournal(models.Model):
    _inherit = "account.journal"

    bank_statements_source = fields.Selection(
        selection_add=[('p24b_import', _('Privat24Business Import'))])
    p24_login = fields.Char(string='Privat24 Login')
    p24_passwd = fields.Char(string='Privat24 Password')

    @api.multi
    def p24b_sync_statement(self):
        login = ''
        passwd = ''
        if not self.bank_acc_number:
            raise UserError(_(u'Provide account number on bank journal!'))
        if self.p24_login:
            login = base64.b64decode(self.p24_login)
        if self.p24_passwd:
            passwd = base64.b64decode(self.p24_passwd)
        initial_values = {
            'journal_id': self.id,
            'bank_acc': self.bank_acc_number,
            'state': 'success',
            'task': 'statement_import',
            'login': login,
            'passwd': passwd
        }

        p24b = self.env['account.p24b.sync'].create(initial_values)
        return p24b.do_sync()

    @api.multi
    def write(self, vals):
        if 'p24_login' in vals:
            # encode field
            vals['p24_login'] = base64.b64encode(vals['p24_login'])
        if 'p24_passwd' in vals:
            # encode field
            vals['p24_passwd'] = base64.b64encode(vals['p24_passwd'])
        return super(P24AccountJournal, self).write(vals)

    @api.model
    def create(self, vals):
        if 'p24_login' in vals:
            if vals['p24_login']:
                # encode field
                vals['p24_login'] = base64.b64encode(vals['p24_login'])
        if 'p24_passwd' in vals:
            if vals['p24_passwd']:
                # encode field
                vals['p24_passwd'] = base64.b64encode(vals['p24_passwd'])
        return super(P24AccountJournal, self).create(vals)

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        data = super(P24AccountJournal, self).read(fields=fields, load=load)
        for vals in data:
            if 'p24_login' in vals:
                if vals['p24_login']:
                    vals['p24_login'] = base64.b64decode(vals['p24_login'])
            if 'p24_passwd' in vals:
                if vals['p24_passwd']:
                    vals['p24_passwd'] = base64.b64decode(vals['p24_passwd'])
        return data
