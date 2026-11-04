from psycopg2 import IntegrityError
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged('post_install', '-at_install')
class TestBd(TransactionCase):
    def test_ref_and_niu(self):
        a = self.env['bd.partenaire'].create({'name': 'Alpha', 'niu': ' m123 '})
        b = self.env['bd.partenaire'].create({'name': 'Beta'})
        self.assertRegex(a.ref, r'^P-\d{4}$')
        self.assertNotEqual(a.ref, b.ref)
        self.assertEqual(a.niu, 'M123')
        self.assertIn(a.ref, a.display_name)
        self.assertEqual(self.env['bd.partenaire'].name_search(a.ref)[0][0], a.id)
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'), self.cr.savepoint():
            self.env['bd.partenaire'].create({'name': 'Dup', 'niu': 'M123'})

    def test_search_and_compare(self):
        P = self.env['bd.partenaire']
        a = P.create({'name': 'Alpha', 'status': 'agree'})
        b = P.create({'name': 'Beta'})
        c = P.create({'name': 'Gamma', 'status': 'suspendu'})
        for p, price in ((a, 50), (b, 40), (c, 10)):
            self.env['bd.partenaire.article'].create({'partenaire_id': p.id, 'name': 'Ciment', 'prix_unitaire': price})
        w = self.env['bd.partenaire.search.wizard'].create({'article_search': 'ciment'})
        self.assertEqual(set(P.search(w.action_search()['domain'])), {a, b})
        arts = self.env['bd.partenaire.article'].search(w.action_compare()['domain'], order='prix_unitaire')
        self.assertEqual(arts.mapped('prix_unitaire'), [40, 50])
        w.only_agree = True
        self.assertEqual(P.search(w.action_search()['domain']), a)
        a.contact_ids = [(0, 0, {'name': 'Jean'}), (0, 0, {'name': 'Marie'})]
        self.assertEqual(len(a.contact_ids), 2)

    def test_exports(self):
        a = self.env['bd.partenaire'].create({'name': 'Alpha'})
        self.assertTrue(a.action_export_xlsx()['url'])
        html, _ = self.env['ir.actions.report']._render_qweb_html('adk_bd_partenaire.action_report_bd_partenaire_fiche', a.ids)
        self.assertIn(b'Alpha', html)
