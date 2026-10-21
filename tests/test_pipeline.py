"""Test nominal fourni. Ajouter au moins un test de réponse modèle mal formée."""
import unittest
from pipeline import analyze, load_context
from check_output import validate, validate_documents

class PipelineTests(unittest.TestCase):
    def test_simulated_report_contract(self):
        context=load_context('E01')
        report=analyze('E01', mode='simule')
        validate(report,context['entretien'],context['produits'],context['regles'])
        validate_documents(report,context['index_documents'])
        self.assertEqual(report['diagnostic']['mode'],'simule')
        self.assertFalse(report['diagnostic']['appel_modele_effectue'])

if __name__=='__main__': unittest.main()
