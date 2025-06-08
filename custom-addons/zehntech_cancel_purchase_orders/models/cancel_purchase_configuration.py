from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CancelPurchaseConfiguration(models.Model):
    _name = 'cancel.purchase.configuration'
    _description = 'Cancel Purchase Configuration'


    enable_feature = fields.Boolean(
        string="Enable Cancel Purchase for Users",
        default=True,
        help="Enable or disable cancel functionalities for non-admin users."
    )
    default_reason = fields.Char(
        string="Default Cancellation Reason",
        help="Specify a default reason for cancellations."
    )

    @api.model_create_multi
    def create(self, vals_list):
        # Only one configuration record allowed.
        existing = self.search([], limit=1)
        if existing:
            for vals in vals_list:
                existing.write(vals)
            return existing
        return super(CancelPurchaseConfiguration, self).create(vals_list)

    @api.constrains('enable_feature')
    def _check_singleton(self):
        if self.search_count([]) > 1:
            raise ValidationError(_("Only one Cancel Purchase Configuration record can exist!"))

    @api.model
    def toggle_feature(self):
        config = self.search([], limit=1)
        if not config:
            config = self.create([{'enable_feature': False}])[0]
        config.enable_feature = not config.enable_feature

    @api.model
    def get_current_state(self):
        config = self.search([], limit=1)
        return config.enable_feature if config else False

    @api.model
    def get_default_configuration(self):
        config = self.search([], limit=1)
        if not config:
            config = self.create([{'enable_feature': True}])[0]
        return config
