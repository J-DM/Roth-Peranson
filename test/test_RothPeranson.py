import unittest

import pandas as pd

from match.RothPeranson import MatchController

class ResultsTest(unittest.TestCase):

	def test_final_results(self):
		program_choices_test_data = './test/program_choices_test.csv'
		candidate_choices_test_data = './test/candidate_choices_test.csv'
		program_places_test_data = './test/program_places.csv'

		test_match = MatchController(program_choices_test_data, candidate_choices_test_data, program_places_test_data)
		test_match.start_match()
		results = test_match.results_dict()

		self.assertEqual(results['Anderson'], 'Did not match')
		self.assertEqual(results['Beaudry'], 'Did not match')
		self.assertEqual(results['Chen'], 'Mercy')
		self.assertEqual(results['Davis'], 'General')
		self.assertEqual(results['Eastman'], 'City')
		self.assertEqual(results['Feldman'], 'State')
		self.assertEqual(results['Garcia'], 'City')
		self.assertEqual(results['Hassan'], 'State')


if __name__ == '__main__':
	unittest.main()