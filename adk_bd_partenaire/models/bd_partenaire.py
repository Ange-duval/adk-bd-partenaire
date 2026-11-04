# -*- coding: utf-8 -*-
import base64
import io

from odoo import models, fields, api
from odoo.exceptions import UserError


class BdPartenaire(models.Model):
    _name = 'bd.partenaire'
    _description = "BD Partenaire - Fiche Partenaire"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'name'

    # --- Identité ---
    ref = fields.Char(string="Réf.", copy=False, readonly=True, default='/', index=True,
                      help="Référence courte et unique, attribuée automatiquement (ex : P-0001).")
    name = fields.Char(string="Nom / Raison Sociale", required=True, tracking=True)
    status = fields.Selection([
        ('evaluation', 'En évaluation'),
        ('agree', 'Agréé'),
        ('suspendu', 'Suspendu'),
    ], string="Statut", default='evaluation', required=True, tracking=True, index=True,
        help="Seuls les partenaires non suspendus apparaissent dans la recherche des acheteurs.")
    company_id = fields.Many2one('res.company', string="Société", default=lambda self: self.env.company)
    contact_ids = fields.One2many('bd.partenaire.contact', 'partenaire_id', string="Interlocuteurs")
    sigle = fields.Char(string="Sigle / Nom Commercial")
    image_1920 = fields.Image(string="Logo / Photo", max_width=1920, max_height=1920)
    active = fields.Boolean(default=True)

    # --- Identification légale ---
    niu = fields.Char(string="NIU", help="Numéro d'Identifiant Unique.", tracking=True)
    rccm = fields.Char(string="RCCM", help="Registre du Commerce et du Crédit Mobilier.", tracking=True)
    regime_fiscal_id = fields.Many2one('bd.partenaire.regime.fiscal', string="Régime Fiscal", tracking=True)
    forme_juridique_id = fields.Many2one('bd.partenaire.legal.form', string="Forme Juridique")

    # --- Classification ---
    partner_role = fields.Selection([
        ('fournisseur', 'Fournisseur'),
        ('client', 'Client'),
        ('les_deux', 'Fournisseur & Client'),
    ], string="Type de Partenaire", default='fournisseur', required=True, tracking=True)
    domaine_activite_ids = fields.Many2many(
        'bd.partenaire.activity.domain', 'bd_partenaire_activity_domain_rel',
        'partenaire_id', 'domain_id', string="Domaine(s) d'Activité")
    categorie_ids = fields.Many2many(
        'bd.partenaire.category', 'bd_partenaire_category_rel',
        'partenaire_id', 'category_id', string="Catégorie(s)")

    # --- Coordonnées ---
    street = fields.Char(string="Adresse")
    street2 = fields.Char(string="Adresse (suite)")
    city = fields.Char(string="Ville")
    state_id = fields.Many2one('res.country.state', string="Région / Département")
    zip = fields.Char(string="Code Postal / BP")
    country_id = fields.Many2one('res.country', string="Pays")
    phone = fields.Char(string="Téléphone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    website = fields.Char(string="Site Web")

    # --- Interlocuteur principal ---
    contact_name = fields.Char(string="Nom de l'Interlocuteur")
    contact_function = fields.Char(string="Fonction")
    contact_phone = fields.Char(string="Téléphone Direct")
    contact_email = fields.Char(string="Email Direct")

    # --- Informations bancaires ---
    bank_name = fields.Char(string="Banque")
    bank_account = fields.Char(string="N° Compte / IBAN")

    # --- Suivi interne ---
    date_registration = fields.Date(string="Date d'Enregistrement", default=fields.Date.context_today)
    registered_by = fields.Many2one('res.users', string="Enregistré par", default=lambda self: self.env.user)
    note = fields.Text(string="Notes Internes")

    # --- Catalogue d'articles / services ---
    article_ids = fields.One2many('bd.partenaire.article', 'partenaire_id', string="Articles / Services")
    article_count = fields.Integer(compute='_compute_article_count', string="Nb. Articles")

    # --- Badges & Classement ---
    badge_assignment_ids = fields.One2many(
        'bd.partenaire.badge.assignment', 'partenaire_id', string="Attributions de Badges")
    badge_ids = fields.Many2many(
        'bd.partenaire.badge', compute='_compute_badges', string="Badges Actifs", store=True)
    badge_count = fields.Integer(compute='_compute_badges', string="Nb. Badges", store=True)
    total_points = fields.Integer(compute='_compute_badges', string="Score Total", store=True)
    top_badge_id = fields.Many2one(
        'bd.partenaire.badge', compute='_compute_badges', string="Badge Principal", store=True)

    _sql_constraints = [
        ('niu_uniq', 'unique(niu, company_id)', "Ce NIU existe déjà dans la base partenaires."),
        ('ref_uniq', 'unique(ref, company_id)', "Cette référence existe déjà."),
    ]

    @api.depends('ref', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = '[%s] %s' % (rec.ref, rec.name) if rec.ref and rec.ref != '/' else rec.name

    @api.model
    def _search_display_name(self, operator, value):
        if value and operator in ('ilike', 'like', '=', '=ilike'):
            return ['|', '|', ('ref', operator, value), ('name', operator, value), ('sigle', operator, value)]
        return super()._search_display_name(operator, value)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == '/':
                vals['ref'] = self.env['ir.sequence'].next_by_code('bd.partenaire') or '/'
            if vals.get('niu'):
                vals['niu'] = vals['niu'].strip().upper()
            elif 'niu' in vals:
                vals['niu'] = False
        return super().create(vals_list)

    def write(self, vals):
        if 'niu' in vals:
            vals['niu'] = (vals['niu'] or '').strip().upper() or False
        return super().write(vals)

    def action_set_status(self):
        status = self.env.context.get('status')
        if status:
            self.write({'status': status})

    @api.depends('article_ids')
    def _compute_article_count(self):
        for rec in self:
            rec.article_count = len(rec.article_ids)

    @api.depends('badge_assignment_ids.active', 'badge_assignment_ids.badge_id',
                 'badge_assignment_ids.points')
    def _compute_badges(self):
        for rec in self:
            active_assign = rec.badge_assignment_ids.filtered('active')
            badges = active_assign.mapped('badge_id')
            rec.badge_ids = badges
            rec.badge_count = len(badges)
            rec.total_points = sum(active_assign.mapped('points'))
            rec.top_badge_id = badges.sorted('points_min', reverse=True)[:1]

    def action_view_articles(self):
        self.ensure_one()
        return {
            'name': "Articles de %s" % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'bd.partenaire.article',
            'view_mode': 'list,form',
            'domain': [('partenaire_id', '=', self.id)],
            'context': {'default_partenaire_id': self.id},
        }

    def action_view_badge_assignments(self):
        self.ensure_one()
        return {
            'name': "Badges de %s" % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'bd.partenaire.badge.assignment',
            'view_mode': 'list,form',
            'domain': [('partenaire_id', '=', self.id)],
            'context': {'default_partenaire_id': self.id},
        }

    def action_open_assign_badge_wizard(self):
        self.ensure_one()
        return {
            'name': "Attribuer un Badge à %s" % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'bd.partenaire.badge.assign.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_partenaire_id': self.id},
        }

    def action_export_xlsx(self):
        """Exporte la sélection (ou tous les partenaires visibles) en Excel."""
        try:
            import xlsxwriter
        except ImportError:
            raise UserError(self.env._("La bibliothèque Python xlsxwriter est requise pour l'export Excel."))
        records = self or self.search([])
        out = io.BytesIO()
        wb = xlsxwriter.Workbook(out, {'in_memory': True})
        ws = wb.add_worksheet('Partenaires')
        head = wb.add_format({'bold': True, 'bg_color': '#5B21B6', 'font_color': '#FFFFFF', 'border': 1})
        cell = wb.add_format({'border': 1})
        cols = [('Réf.', lambda r: r.ref), ('Nom', lambda r: r.name), ('Statut', lambda r: dict(r._fields['status'].selection).get(r.status)),
                ('Type', lambda r: dict(r._fields['partner_role'].selection).get(r.partner_role)), ('NIU', lambda r: r.niu),
                ('RCCM', lambda r: r.rccm), ('Ville', lambda r: r.city), ('Téléphone', lambda r: r.phone or r.mobile),
                ('Email', lambda r: r.email), ('Interlocuteurs', lambda r: ', '.join(r.contact_ids.mapped('name'))),
                ('Score', lambda r: r.total_points)]
        for c, (label, _f) in enumerate(cols):
            ws.write(0, c, label, head)
            ws.set_column(c, c, 22)
        for i, rec in enumerate(records, start=1):
            for c, (_label, f) in enumerate(cols):
                ws.write(i, c, f(rec) or '', cell)
        wb.close()
        att = self.env['ir.attachment'].create({
            'name': 'Partenaires.xlsx', 'type': 'binary', 'datas': base64.b64encode(out.getvalue()),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
        return {'type': 'ir.actions.act_url', 'url': '/web/content/%s?download=true' % att.id, 'target': 'self'}
