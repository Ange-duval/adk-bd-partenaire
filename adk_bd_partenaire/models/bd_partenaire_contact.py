# -*- coding: utf-8 -*-
from odoo import fields, models


class BdPartenaireContact(models.Model):
    _name = 'bd.partenaire.contact'
    _description = "BD Partenaire - Interlocuteur"
    _order = 'sequence, id'

    partenaire_id = fields.Many2one('bd.partenaire', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Nom", required=True)
    function = fields.Char(string="Fonction")
    phone = fields.Char(string="Téléphone")
    email = fields.Char(string="Email")
