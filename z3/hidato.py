#!/usr/bin/python -u
# -*- coding: latin-1 -*-
# 
# Hidato puzzle in Z3
# http://www.shockwave.com/gamelanding/hidato.jsp
# http://www.hidato.com/
# '''
# Puzzles start semi-filled with numbered tiles.
# The first and last numbers are circled.
# Connect the numbers together to win. Consecutive
# number must touch horizontally, vertically, or
# diagonally.
# '''
#
# Time to first solution:
#
# puzzle1 : 0.0412900447845459
# puzzle2 : 3.2280960083007812
# puzzle3 : 0.31029653549194336
# puzzle4 : 0.26546549797058105
# puzzle5 : 1.6768722534179688
# puzzle6 : 11.532785654067993
# puzzle7 : 86.42020177841187
# puzzle8 : 356.0383880138397

# 
# Time to prove unicity:
# puzzle1 : 0.042975664138793945
# puzzle2 : 3.936161994934082
# puzzle3 : 0.340954065322876
# puzzle4 : 0.26323676109313965
# puzzle5 : 1.8561887741088867
# puzzle6 : 13.294347524642944
# puzzle7 : 92.71803569793701
# puzzle8 : 414.0651047229767
# 
#
#
# Note: This model is quite slow.
# See hidato_table.py and hidato_function.py for faster programs.
#
# See hidato_function.py for a comparison of the Hidato solvers.
#
# 
# This Z3 model was written by Hakan Kjellerstrand (hakank@gmail.com)
# See also my Z3 page: http://hakank.org/z3/
# 
from __future__ import print_function
import time
from hidato_instances import instances
from z3_utils_hakank import *


def hidato(puzzle,num_sols=0):

  sol = SimpleSolver()

  r = len(puzzle)
  c = len(puzzle[0])

  print_game(puzzle, r, c)

  #
  # declare variables
  #
  x = {}
  for i in range(r):
    for j in range(c):
      x[(i, j)] = makeIntVar(sol, "x(%i,%i)" % (i, j), 1, r * c)
  x_flat = [x[(i, j)] for i in range(r) for j in range(c)]

  #
  # constraints
  #
  sol.add(Distinct(x_flat))

  #
  # Fill in the clues
  #
  for i in range(r):
    for j in range(c):
      if puzzle[i][j] > 0:
        sol.add(x[(i, j)] == puzzle[i][j])

  # From the numbers k = 1 to r*c-1, find this position,
  # and then the position of k+1
  cc = 0
  for k in range(1, r * c):
    i = makeIntVar(sol,"i_tmp_%i_%i" % (k,cc), 0, r-1)
    j = makeIntVar(sol,"j_tmp_%i_%i" % (k,cc), 0, c-1)
    a = makeIntVar(sol,"a_tmp_%i_%i" % (k,cc), -1, 1)
    b = makeIntVar(sol,"b_tmp_%i_%i" % (k,cc), -1, 1)
    cc += 1

    # 1) First: fix "this" k
    # sol.add(k == x[(i,j)])
    element(sol,i * c + j,x_flat,k,r*c)
   
    # 2) and then find the position of the next value (k+1)
    # solver.add(k + 1 == x[(i+a,j+b)])
    element(sol,(i + a) * c + (j + b),x_flat, k + 1,r*c)

    sol.add(i + a >= 0)
    sol.add(j + b >= 0)
    sol.add(i + a < r)
    sol.add(j + b < c)

    sol.add(Or(a != 0, b != 0))

  #
  # solution and search
  #
  num_solutions = 0
  while sol.check() == sat:
    num_solutions += 1
    mod = sol.model()
    xx_flat =  [mod.eval(x_flat[i*c+j]) for i in range(r) for j in range(c)]
    print("\nSolution:", num_solutions)
    print_board(mod, x, r, c)
    print()
    if num_sols > 0 and num_solutions >= num_sols:
      break
    sol.add(Or([xx_flat[i*c+j] != x_flat[i*c+j] for i in range(r) for j in range(c) ]))

  print("num_solutions:", num_solutions)


def print_board(mod, x, rows, cols):
  for i in range(rows):
    for j in range(cols):
      print("% 3s" % mod.eval(x[i,j]), end=' ')
    print("")


def print_game(game, rows, cols):
  for i in range(rows):
    for j in range(cols):
      print("% 3s" % game[i][j], end=' ')
    print("")


def test_all(num_sols=0):
  times = {}
  for puzzle in instances:
    print()
    print(f"----- Solving problem {puzzle} -----")
    print()
    t0 = time.time()
    hidato(instances[puzzle],num_sols)
    t1 = time.time()
    print("Time:", t1-t0)
    times[puzzle] = t1-t0
    print()

  print("Times:")
  for puzzle in times:
    print(puzzle, ":", times[puzzle])

print("\nTime to first solution:")
num_sols = 1
test_all(num_sols)

print("Time to prove unicity:")
num_sols = 0
test_all(num_sols)

