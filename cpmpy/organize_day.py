"""
Organizing a day in cpmpy.

Simple scheduling problem.

Problem formulation from ECLiPSe:
Slides on (Finite Domain) Constraint Logic Programming, page 38f
http://eclipse-clp.org/reports/eclipse.ppt


This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import cpmpy.solvers
import numpy as np
from cpmpy_hakank import *


#
# No overlapping of tasks s1 and s2
#


def no_overlap(s1, d1, s2, d2):
  return [(s1 + d1 <= s2) | (s2 + d2 <= s1)]


def organize_day():

  model = Model()

  
  # data
  n = 4

  tasks = list(range(n))
  work, mail, shop, bank = tasks
  durations = [4, 1, 2, 1]

  # task [i,0] must be finished before task [i,1]
  before_tasks = [[bank, shop], [mail, work]]

  # the valid times of the day
  begin = 9
  end = 17

  # declare variables
  begins = intvar(begin,end,shape=n,name="begins")
  ends = intvar(begin,end,shape=n,name="ends")

  # constraints
  model += [ends[i] == begins[i] + durations[i] for i in tasks]
  model += [no_overlap(begins[i], durations[i], begins[j], durations[j])
             for i in tasks
             for j in tasks
             if i < j]
    
  # specific constraints
  # dependencies
  model += [ends[before] <= begins[after] for (before, after) in before_tasks]
  # special task
  model += [begins[work] >= 11]

  ss = CPM_ortools(model)
  num_solutions = 0
  while ss.solve():
    num_solutions += 1
    print("begins:", begins.value())
    print("ends:", ends.value())
    print()
    get_different_solution(ss,flatten_lists([begins,ends]))

  print('num_solutions:', num_solutions)


organize_day()