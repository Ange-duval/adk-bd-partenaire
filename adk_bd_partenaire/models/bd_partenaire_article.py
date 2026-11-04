# -*- coding: utf-8 -*-
from odoo import models, fields


class BdPartenaireArticle(models.Model):
    _name = 'bd.partenaire.article'
    _description = "BD Partenaire - Article / Service Fourni"
    _order = 'name'

    partenaire_id = fields.Many2one(
        'bd.partenaire', string="Partenaire", required=True, ondelete='cascade')
    name = fields.Char(string="Désignation", required=True)
    reference = fields.Char(string="Référence")
    article_categorie_id = fields.Many2one(
        'bd.partenaire.article.category', string="Catégorie d'Article / Type d'Achat")
    description = fields.Text(string="Description")
    unite = fields.Char(string="Unité", help="Ex : pièce, kg, m², heure, service, forfait...")
    prix_unitaire = fields.Float(string="Prix Unitaire")
    currency_id = fields.Many2one(
        'res.currency', string="Devise", default=lambda self: self.env.company.currency_id)
    disponibilite = fields.Selection([
        ('disponible', 'Disponible'),
        ('rupture', 'Rupture de Stock'),
        ('sur_commande', 'Sur Commande'),
    ], string="Disponibilité", default='disponible')
    delai_livraison_jours = fields.Integer(string="Délai de Livraison (jours)")
    date_maj = fields.Date(string="Dernière Mise à Jour", default=fields.Date.context_today)
    active = fields.Boolean(default=True)
