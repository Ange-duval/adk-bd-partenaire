# -*- coding: utf-8 -*-
from odoo import models, fields


class BdPartenaireRegimeFiscal(models.Model):
    _name = 'bd.partenaire.regime.fiscal'
    _description = "BD Partenaire - Régime Fiscal"
    _order = 'sequence, name'

    name = fields.Char(string="Régime Fiscal", required=True)
    code = fields.Char(string="Code")
    sequence = fields.Integer(string="Séquence", default=10)
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Ce régime fiscal existe déjà."),
    ]


class BdPartenaireLegalForm(models.Model):
    _name = 'bd.partenaire.legal.form'
    _description = "BD Partenaire - Forme Juridique"
    _order = 'name'

    name = fields.Char(string="Forme Juridique", required=True)
    code = fields.Char(string="Code")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Cette forme juridique existe déjà."),
    ]


class BdPartenaireActivityDomain(models.Model):
    _name = 'bd.partenaire.activity.domain'
    _description = "BD Partenaire - Domaine d'Activité"
    _order = 'complete_name'

    name = fields.Char(string="Domaine d'Activité", required=True)
    code = fields.Char(string="Code")
    parent_id = fields.Many2one('bd.partenaire.activity.domain', string="Domaine Parent", ondelete='cascade')
    child_ids = fields.One2many('bd.partenaire.activity.domain', 'parent_id', string="Sous-domaines")
    complete_name = fields.Char(string="Nom Complet", compute='_compute_complete_name', store=True, recursive=True)
    active = fields.Boolean(default=True)

    def _compute_complete_name(self):
        for rec in self:
            rec.complete_name = "%s / %s" % (rec.parent_id.complete_name, rec.name) if rec.parent_id else rec.name


class BdPartenaireCategory(models.Model):
    _name = 'bd.partenaire.category'
    _description = "BD Partenaire - Catégorie Partenaire"
    _order = 'name'

    name = fields.Char(string="Catégorie", required=True)
    code = fields.Char(string="Code")
    color = fields.Integer(string="Couleur")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Cette catégorie existe déjà."),
    ]


class BdPartenaireArticleCategory(models.Model):
    _name = 'bd.partenaire.article.category'
    _description = "BD Partenaire - Catégorie d'Article / Type d'Achat"
    _order = 'name'

    name = fields.Char(string="Catégorie d'Article", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Cette catégorie d'article existe déjà."),
    ]
