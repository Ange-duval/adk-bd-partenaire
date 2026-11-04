# -*- coding: utf-8 -*-
from odoo import models, fields


class BdPartenaireSearchWizard(models.TransientModel):
    _name = 'bd.partenaire.search.wizard'
    _description = "BD Partenaire - Assistant de Recherche (Acheteuse)"

    article_search = fields.Char(
        string="Article / Service Recherché",
        help="Recherche dans la désignation, la référence et la description des articles.")
    article_categorie_id = fields.Many2one(
        'bd.partenaire.article.category', string="Catégorie d'Article / Type d'Achat")
    domaine_activite_ids = fields.Many2many(
        'bd.partenaire.activity.domain', string="Domaine d'Activité")
    categorie_ids = fields.Many2many('bd.partenaire.category', string="Catégorie de Partenaire")
    regime_fiscal_id = fields.Many2one('bd.partenaire.regime.fiscal', string="Régime Fiscal")
    forme_juridique_id = fields.Many2one('bd.partenaire.legal.form', string="Forme Juridique")
    score_min = fields.Integer(string="Score Minimum")
    city = fields.Char(string="Ville")
    only_agree = fields.Boolean(string="Partenaires agréés uniquement")

    def action_compare(self):
        """Liste des articles des partenaires retenus, du moins cher au plus cher."""
        self.ensure_one()
        partner_domain, article_domain = self._build_domain()
        partners = self.env['bd.partenaire'].search(partner_domain)
        return {
            'name': "Comparaison des offres",
            'type': 'ir.actions.act_window',
            'res_model': 'bd.partenaire.article',
            'view_mode': 'list',
            'views': [(self.env.ref('adk_bd_partenaire.view_bd_partenaire_article_compare_list').id, 'list')],
            'domain': article_domain + [('partenaire_id', 'in', partners.ids)],
        }

    def action_search(self):
        domain, _article_domain = self._build_domain()
        return {
            'name': "Partenaires Correspondants",
            'type': 'ir.actions.act_window',
            'res_model': 'bd.partenaire',
            'view_mode': 'list,kanban,form',
            'domain': domain,
            'target': 'current',
        }

    def _build_domain(self):
        self.ensure_one()
        domain = [('partner_role', 'in', ['fournisseur', 'les_deux']), ('status', '!=', 'suspendu')]
        if self.only_agree:
            domain.append(('status', '=', 'agree'))
        if self.city:
            domain.append(('city', 'ilike', self.city))

        if self.domaine_activite_ids:
            domain.append(('domaine_activite_ids', 'in', self.domaine_activite_ids.ids))
        if self.categorie_ids:
            domain.append(('categorie_ids', 'in', self.categorie_ids.ids))
        if self.regime_fiscal_id:
            domain.append(('regime_fiscal_id', '=', self.regime_fiscal_id.id))
        if self.forme_juridique_id:
            domain.append(('forme_juridique_id', '=', self.forme_juridique_id.id))
        if self.score_min:
            domain.append(('total_points', '>=', self.score_min))

        if self.article_search or self.article_categorie_id:
            article_domain = []
            if self.article_search:
                article_domain += ['|', '|',
                                    ('name', 'ilike', self.article_search),
                                    ('reference', 'ilike', self.article_search),
                                    ('description', 'ilike', self.article_search)]
            if self.article_categorie_id:
                article_domain.append(('article_categorie_id', '=', self.article_categorie_id.id))
            matching_partenaires = self.env['bd.partenaire.article'].search(article_domain).mapped('partenaire_id')
            domain.append(('id', 'in', matching_partenaires.ids))
        else:
            article_domain = []
        return domain, article_domain
