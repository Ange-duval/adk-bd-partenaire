# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BdPartenaireBadge(models.Model):
    _name = 'bd.partenaire.badge'
    _description = "BD Partenaire - Badge / Distinction"
    _order = 'sequence, points_min desc'

    name = fields.Char(string="Nom du Badge", required=True)
    code = fields.Char(string="Code")
    sequence = fields.Integer(string="Séquence", default=10)
    icon = fields.Char(string="Icône (emoji)", default="🏆")
    color = fields.Integer(string="Couleur")
    points_min = fields.Integer(
        string="Seuil de Points",
        help="Score minimum suggéré pour l'obtention de ce badge.")
    description = fields.Text(string="Description / Critères d'attribution")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Ce badge existe déjà."),
    ]


class BdPartenaireBadgeAssignment(models.Model):
    _name = 'bd.partenaire.badge.assignment'
    _description = "BD Partenaire - Attribution de Badge"
    _order = 'date_assignment desc'
    _rec_name = 'display_name'

    partenaire_id = fields.Many2one(
        'bd.partenaire', string="Partenaire", required=True, ondelete='cascade')
    badge_id = fields.Many2one(
        'bd.partenaire.badge', string="Badge", required=True, ondelete='restrict')
    date_assignment = fields.Date(
        string="Date d'Attribution", default=fields.Date.context_today, required=True)
    period_label = fields.Char(string="Période", help="Ex : 2026, T1 2026...")
    points = fields.Integer(string="Points", default=0)
    note = fields.Text(string="Motif / Commentaire")
    assigned_by = fields.Many2one(
        'res.users', string="Attribué par", default=lambda self: self.env.user)
    active = fields.Boolean(string="Actif", default=True)
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('partenaire_id', 'badge_id', 'period_label')
    def _compute_display_name(self):
        for rec in self:
            label = "%s - %s" % (rec.partenaire_id.name or '', rec.badge_id.name or '')
            if rec.period_label:
                label += " (%s)" % rec.period_label
            rec.display_name = label
