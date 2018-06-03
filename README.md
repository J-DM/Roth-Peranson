
<div align="center">
  <img src="https://raw.github.com/J-DM/Roth-Peranson/readme_files/match.png)"><br>
</div>

# Roth Peranson Match Algorithm

This is an unofficial Python implementation of the Nobel Prize winning algorithm used to match Canadian medical school graduates to residency positions.

## Prerequisites

This is largely standalone, the only requirement being pandas to manage the csv rank order lists.


```
pip install pandas

```

## Example

The test case here is based on the [Carms guide](https://www.carms.ca/the-match/how-it-works/) to the matching algorithm. Print statement have been included as comments if you wish to run a "loud" version of the matching in order to show the search and recursive replacements as they happen.

## Notes

This implements the simple markets, applicant first version of the algorithm. The main differences from the full carms use is the lack of couples matching or second year entry.

## How it works

The algorithm is based on the work of Alvin E. Roth and Elliot Peranson in their paper [__The Redesign of the Matching Market for American Physicians: Some Engineering Aspects of Economic Design__](https://web.stanford.edu/~alroth/papers/rothperansonaer.PDF) as well as previous work on matching markets by David Gale and Lloyd Shaply. Roth and Shapley jointly won the 2012 Nobel Prize in Economics "for the theory of stable allocations and the practice of market design"

The goal is to form "Stable Matches" that is, no candidate and program wish they were matched with each other instead of their actual match. To do this both candidates and programs produce rank order lists of their preferences after which the algorithm progresses through each candidate, down their rank order list, temporarily matching them to the best program which wants them. As students are considered better matches, from the perspective of the program, may displace candidates with a temporary match in which case that candidate progresses down their remaining options potentially displacing others and so on until each students rank order list has been exhausted. At this point all students will either be matched to the best program they can be, relative to their competition, or will have failed to match entirely.

The design of the algorithm minimises the potential for strategic rank order lists, incentivising programs and applicants to state their true preferences.

Further work needs to be done on this implementation to support candidates with complementarities.

## Authors

* **John Dirk Morrison** - *Research and Implementation* - [J-DM](https://github.com/J-DM)

## Acknowledgements

Illustration - Pair-to-Pair by pedro baños cancer from the Noun Project

## Get in touch!

You can reach me at john.dirk.morrison \[you know the thing\] gmail.com 