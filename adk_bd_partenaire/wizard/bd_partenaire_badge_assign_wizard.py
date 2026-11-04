# -*- coding: utf-8 -*-
from odoo import models, fields


class BdPartenaireBadgeAssignWizard(models.TransientModel):
    _name = 'bd.partenaire.badge.assign.wizard'
    _description = "BD Partenaire - Assistant d'Attribution de Badge"

    partenaire_id = fields.Many2one('bd.partenaire', string="Partenaire", required=True)
    badge_id = fields.Many2one('bd.partenaire.badge', string="Badge", required=True)
    period_label = fields.Char(string="Période", help="Ex : 2026, T1 2026...")
    points = fields.Integer(string="Points", default=0)
    note = fields.Text(string="Motif / Commentaire")

    def action_confirm(self):
        self.ensure_one()
        self.env['bd.partenaire.badge.assignment'].create({
            'partenaire_id': self.partenaire_id.id,
            'badge_id': self.badge_id.id,
            'period_label': self.period_label,
            'points': self.points,
            'note': self.note,
        })
        return {'type': 'ir.actions.act_window_close'}
