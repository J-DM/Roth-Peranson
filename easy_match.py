from match.RothPeranson import MatchController

def run_match():
    print("This script uses the files in the easy_match folder.")
    print("You can use them as templates, extending to however many programs/candidates are required.")
    print("The filenames cannot be changed for this script.")
    print("\n")

    program_rol = 'easy_match/program_rank_order_lists.csv'
    candidate_rol = 'easy_match/candidate_rank_order_lists.csv'
    program_places = 'easy_match/program_places.csv'

    match = MatchController(program_rol, candidate_rol, program_places)
    match.start_match()
    results = match.results_dict()

    print(results)
    match.get_output_csv()

if __name__ == '__main__':
    run_match()