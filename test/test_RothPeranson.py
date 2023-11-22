import unittest
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

import pandas as pd

from match.RothPeranson import MatchController

class ResultsTest(unittest.TestCase):

	def run(self, result=None):
		test_method_name = self._testMethodName
		try:
			logging.info(f"{test_method_name}")
			logging.info("")
			super().run(result)  # Run the test
			logging.info("")
			logging.info(f"{test_method_name} - Pass")
			logging.info(" ")
		except AssertionError as e:
			logging.error(f"{test_method_name} - Fail")
			logging.info(" ")
			raise e

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

	def test_retained_assignment_example(self):
		# With thanks to @ebzheng for raising an issue with assignment being retained
		program_choices_test_data = './test/program_choices_cycle_test.csv'
		candidate_choices_test_data = './test/candidate_choices_cycle_test.csv'

		test_match = MatchController(program_choices_test_data, candidate_choices_test_data)
		test_match.start_match()
		results = test_match.results_dict()

		self.assertEqual(results['Anderson'], 'City')
		self.assertEqual(results['Beaudry'], 'General')
		self.assertEqual(results['Chen'], 'University')
		self.assertEqual(results['Davis'], 'Did not match')


if __name__ == '__main__':
	unittest.main()