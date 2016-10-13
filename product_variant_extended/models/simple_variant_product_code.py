import logging
from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from jinja2.sandbox import SandboxedEnvironment
    mako_env = SandboxedEnvironment(
        variable_start_string="${",
        variable_end_string="}",
        trim_blocks=True,               # do not output newline after blocks
    )
    mako_env.globals.update({
        'str': str,
        'len': len,
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'filter': filter,
        'reduce': reduce,
        'map': map,
        'round': round,
        'cmp': cmp,
    })
except ImportError:
    _logger.warning("jinja2 not available, templating features will not work!")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _variant_code(self):
        for record in self:
            record.variant_code = "".join([v.code or v.name for v in
                                           record.attribute_value_ids])

    variant_code = fields.Char(compute='_variant_code')


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    code = fields.Char()


class ProductCodeGenerator(models.TransientModel):
    """Product Code Generator"""
    _name = 'product.code.generator'
    _description = __doc__

    def _get_template_id(self):
        return self._context.get('active_id')

    code_format = fields.Char(help='Simple String Formatter')
    product_template = fields.Many2one(comodel_name='product.template',
                                       default=_get_template_id)

    @api.multi
    def _set_product_template_variables(self, record):
        return {'t': record.product_template}

    @api.multi
    def _set_product_variant_variables(self, product):
        return {'o': product, 'p': product}

    @api.model
    def generate_code(self, variables=None):
        """
        Code in standard format say TE${p.variant_code}ST
        :return:
        """
        variables = {} if variables is None else variables
        for record in self:
            try:
                template = mako_env.from_string(tools.ustr(record.code_format))
            except Exception:
                _logger.info("Failed to load string %r", record.code_format,
                             exc_info=True)
                return
            variables.update(self._set_product_template_variables(record))
            for product in record.product_template.product_variant_ids:
                variables.update(self._set_product_variant_variables(product))
                try:
                    product.default_code = template.render(variables)
                except Exception:
                    _logger.info("Failed to render template %r "
                                 "using values %r" % (template, variables),
                                 exc_info=True)
                    raise UserError(
                        _("Failed to interpret code format %r "
                          "using values %r") % (template, variables))
            record.product_template.message_post(
                body='Product Codes generated using %s' % record.code_format)
        return {'type': 'ir.actions.act_window_close'}
