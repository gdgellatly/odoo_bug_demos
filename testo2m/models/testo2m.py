# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution - module extension
#    Copyright (C) 2010- O4SB (<http://openforsmallbusiness.co.nz>).
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from logging import getLogger

_logger = getLogger(__name__)


class SaleOrderLine(models.Model):
    """inherit sale order line and add methods to support cutlists"""
    _inherit = "sale.order.line"

    testm2o = fields.Many2one(comodel_name='testm2o',
                              inverse_name='order_line_id',
                              string='Test M2O')


class Cutlist(models.Model):
    _name = 'testm2o'

    order_line_id = fields.One2many(comodel_name='sale.order.line',
                                    inverse_name='testm2o',
                                    string='Order Line Reference',
                                    required=True)
    testo2m = fields.One2many(comodel_name='testo2m',
                              inverse_name='testo2m_id')
    name = fields.Char()


class SaleOrderLineCut(models.Model):
    _name = 'testo2m'

    testo2m_id = fields.Many2one(comodel_name='testm2o',
                                 string='Test M2O',
                                 required=True)
    qty = fields.Integer(required=True)
    length = fields.Float(digits=dp.get_precision('Product Unit of Measure'),
                          required=True)
    name = fields.Char('Pack')
