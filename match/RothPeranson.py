import pandas as pd

class Student():
	# Class representing someone making an application.

    # Commented out sections describe the process loudly
    def __init__(self, name, choices):
        self.name = name
        self.choices = choices[::-1]
        self.current_rank = None
        self.current_place = None
        
    def find_next_preference(self):
        # print(self.name, self.current_rank)
        return self.choices.pop()
        
    def find_next(self):
        try:
            program = self.find_next_preference()
        except IndexError:
            self.current_place = None
            # print("{} did not match.".format(self.name))
            return False
        
        # print(self.name, program.name)
        
        if program.apply_to(self):
            # print("{} temp matched to {}".format(self.name, program.name))
            self.current_place = program
            return True
        
        self.find_next()
        
class Program():
	# Class representing some program accepting total_places students

    def __init__(self, name, total_places=2):
        self.name = name
        self.choices = []
        self.current_picks = []
        self.total_places = total_places
        
    def get_insert_point(self, candidate):
        candidate_rank = self.choices.index(candidate)
        current_ranks = [self.choices.index(c) for c in self.current_picks]
        
        for i, r in enumerate(current_ranks):
            if candidate_rank < r:
                return i
        
    def apply_to(self, candidate):
        if candidate in self.choices:
            if len(self.current_picks) < self.total_places:
                self.current_picks.append(candidate)
                self.current_picks = sorted(self.current_picks, key=lambda r: self.choices.index(r))
                candidate.current_place = self
                return True
            
            if self.get_pick_rank(candidate) < self.get_pick_rank(self.current_picks[-1]):
                insert_point = self.get_insert_point(candidate)
                self.current_picks.insert(insert_point, candidate)
                replaced = self.current_picks.pop()
                candidate.curent_place = self
                replaced.find_next()
                return True
                
        return False
        
    def get_pick_rank(self, candidate):
        return self.choices.index(candidate)
        
        
class MatchController():
	# This class manages the processing of rank order lists for Students and Programs
	# in addition to controlling the match process and returning the final results.

    def __init__(self, program_data, candidate_data):
    	# Takes data as pandas dataframes

        self.program_data = program_data
        self.candidate_data = candidate_data

        self.programs = {}
        self.candidates = {}

        for c in self.program_data.columns:
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
        for k, v in self.candidates.items():
            v.find_next()
            
    def print_results(self):
        for c in sorted(self.candidates.keys()):
            print(c)
            try:
                print('    ', self.candidates[c].current_place.name)
            except AttributeError:
                print('    Did not match')

    def results_dict(self):
        results_dict = {}
        
        for k, v in self.candidates.items():
            try:
                results_dict[k] = v.current_place.name
            except AttributeError:
                results_dict[k] = 'Did not match'
                
        return results_dict

