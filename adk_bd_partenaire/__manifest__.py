# -*- coding: utf-8 -*-
{
    'name': "ADK Base Partenaires",
    'version': '18.0.2.0.0',
    'category': 'Operations',
    'summary': "Base de données autonome des partenaires (fournisseurs/clients) de l'entreprise, "
               "indépendante des Contacts/Achats/Ventes natifs.",
    'description': """
ADK BD Partenaire
==================
Module STANDALONE (autonome) de gestion de la base de données des partenaires de
l'entreprise. Il ne dépend PAS des applications natives Contacts, Achats ou Ventes :
c'est une base de données interne, propre à l'entreprise, alimentée et contrôlée par
le comptable / le service en charge, avec ses propres règles de saisie.

Principe :
----------
* Le comptable (ou le service dédié) enregistre chaque partenaire (fournisseur,
  client ou les deux) avec l'intégralité des informations exigées par l'entreprise :
  identité légale, coordonnées, classification, catalogue d'articles/services,
  badges de performance.
* Lorsqu'une acheteuse a besoin d'acheter un article ou un service, elle se rend
  dans la BD Partenaire, filtre par article recherché, catégorie d'article,
  domaine d'activité, régime fiscal, forme juridique, etc. Les partenaires
  correspondants s'affichent : elle analyse et fait son choix.

Fonctionnalités :
------------------
* Fiche Partenaire complète et autonome (bd.partenaire) : identité légale (NIU,
  RCCM, régime fiscal, forme juridique), coordonnées, interlocuteur principal,
  informations bancaires, domaines d'activité et catégories (multi-sélection),
  type (Fournisseur / Client / Les deux)
* Catalogue d'articles/services propre à chaque partenaire (bd.partenaire.article),
  avec catégorie d'article, prix, unité, délai, disponibilité
* Assistant de recherche pour les acheteuses : filtre par article, catégorie
  d'article, domaine d'activité, catégorie, régime fiscal, forme juridique
* Badges & distinctions "Meilleur Partenaire" avec points, historique
  d'attribution et tableau de bord de classement
* Référence courte (P-0001), statut (Agréé / En évaluation / Suspendu), NIU unique, plusieurs interlocuteurs
* Aucune dépendance aux modules Contacts / Achats / Ventes : base 100% autonome
""",
    'author': "Kambeu Henang Ange Duval",
    'website': "",
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/bd_partenaire_sequence_data.xml',
        'data/bd_partenaire_config_data.xml',
        'data/bd_partenaire_badge_data.xml',
        'views/bd_partenaire_config_views.xml',
        'views/bd_partenaire_views.xml',
        'views/bd_partenaire_search_wizard_views.xml',
        'views/bd_partenaire_badge_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
        'report/bd_partenaire_report.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
