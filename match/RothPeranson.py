from __future__ import annotations

import logging

import pandas as pd

# The Student and Program classes should usually only be interacted with through the MatchController class.

class Student():
# Class representing someone making an application.

    # Commented out sections describe the process loudly
    def __init__(self, name, choices) -> None:
        self.name = name
        self.choices = choices[::-1]
        self.current_rank = None
        self.current_place = None

    def find_next_preference(self) -> Program:
        next_preference = self.choices.pop()
        logging.debug(f"Next preference of {self.name} is {next_preference.name}")
        return next_preference

    def find_next(self) -> bool:
        try:
            program = self.find_next_preference()
        except IndexError:
            self.current_place = None
            logging.debug(f"{self.name} did not match.")
            return False

        if program.apply_to(self):
            return True

        self.find_next()

class Program():
# Class representing some program accepting total_places students

    def __init__(self, name, total_places=1) -> None:
        self.name = name
        self.choices = []
        self.current_picks = []
        self.total_places = total_places

    def get_insert_point(self, candidate) -> int:
        candidate_rank = self.choices.index(candidate)
        current_ranks = [self.choices.index(c) for c in self.current_picks]

        for i, r in enumerate(current_ranks):
            if candidate_rank < r:
                return i

    def apply_to(self, candidate) -> bool:
        if candidate in self.choices:
            if len(self.current_picks) < self.total_places:
                self.current_picks.append(candidate)
                logging.debug(f"{candidate.name} temp matched to {self.name}")
                candidate.current_place = self
                return True

            if self.get_pick_rank(candidate) < self.get_pick_rank(self.current_picks[-1]):
                insert_point = self.get_insert_point(candidate)
                self.current_picks.insert(insert_point, candidate)
                replaced = self.current_picks.pop()
                candidate.current_place = self
                logging.debug(f"{replaced.name} replaced by {candidate.name} at {self.name}")
                replaced.find_next()
                return True

        return False

    def get_pick_rank(self, candidate) -> int:
        return self.choices.index(candidate)


class MatchController():
# This class manages the processing of rank order lists for Students and Programs
# in addition to controlling the match process and returning the final results.

    def __init__(self, program_data, candidate_data, places_data=None) -> None:
    	# Takes csv data directories

        self.program_data = pd.read_csv(program_data)
        self.candidate_data = pd.read_csv(candidate_data)
        if places_data:
            self.places_data = pd.read_csv(places_data, index_col=0)

        self.programs = {}
        self.candidates = {}

        for c in self.program_data.columns:
            if places_data:
                self.programs[c] = Program(c, self.places_data.loc[c].places)
            else:
                self.programs[c] = Program(c)

        for c in self.candidate_data.columns:
            choices = self.candidate_data[c].dropna().tolist()
            choice_objects = [self.programs[p] for p in choices]
            self.candidates[c] = Student(c, choice_objects)

        for c in self.program_data.columns:
            choices = self.program_data[c].dropna().tolist()
            choice_objects = [self.candidates[c] for c in choices]
            self.programs[c].choices = choice_objects

    def start_match(self):
        for _, v in self.candidates.items():
            v.find_next()

    def print_results(self):
        for c in sorted(self.candidates.keys()):
            print(c)
            try:
                print('    ', self.candidates[c].current_place.name)
            except AttributeError:
                print('    Did not match')

    def results_dict(self) -> dict:
        results_dict = {}

        for k, v in self.candidates.items():
            try:
                results_dict[k] = v.current_place.name
            except AttributeError:
                results_dict[k] = 'Did not match'

        return results_dict

    def get_output_csv(self) -> None:
        results = self.results_dict()

        results_df = pd.DataFrame.from_dict(
            results,
            orient='index'
        )

        results_df = results_df.reset_index()
        results_df.columns = ['Candidate', 'Matched Program']

        results_df.to_csv('easy_match/results.csv', index=False)
