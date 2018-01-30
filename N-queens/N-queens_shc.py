#!/usr/bin/env python

import numpy as np
import time
from queue import PriorityQueue

class N_queens:
	
	def __init__(self,size):
		self.size = size
		self.state = []
		self.heuristic = 0
		self.tempstate = []
	
	def random_initial_State(self):
		self.state = np.random.randint(self.size, size=self.size)
		self.tempstate = self.state[:]

	def heuristic_calculator(self):
		self.heuristic=10
		for i in range(len(self.tempstate)):
			for j in range(i+1,len(self.tempstate)):
				if self.tempstate[i]==self.tempstate[j] or np.abs(self.tempstate[i]-self.tempstate[j])==np.abs(i-j):
					self.heuristic+=1
		if(self.heuristic == 10):
			self.heuristic = 0

	def moveQueen_simulate(self,Queen_column,direction,steps):
		# 1-up
		# 2-down
		self.tempstate = self.state[:]
		if direction == 1 and self.tempstate[Queen_column]+steps<self.size:
			self.tempstate[Queen_column] += steps
		if direction == 2 and self.tempstate[Queen_column]-steps>=0:
			self.tempstate[Queen_column] -= steps
	# first move queen and compute cost after movement

	def moveQueen_actual(self):
		self.state = self.tempstate[:]

class Hill_climbing(N_queens):

	def __init__ (self,size):
		N_queens.__init__(self,size)
		self.random_initial_State()
		self.heuristic_calculator()
		self.heuristic_0 = self.heuristic
		self.decision = []
		self.time = 0

	def restart(self):
		return self.random_initial_State()

	def solve(self):
		for i in range(100):
			print("Iteration",i)
			self.time = time.time() + 10
			while self.heuristic>0:
				for i in range(len(self.state)):
					for j in [1,2]:
						self.moveQueen_simulate(i,j,1)
						self.heuristic_calculator()
						if self.heuristic<self.heuristic_0:
							self.heuristic_0 = self.heuristic
							self.decision = [i,j]
				if self.decision:
					self.moveQueen_simulate(self.decision[0],self.decision[1],1)
					self.moveQueen_actual()
					self.heuristic_calculator()
				if time.time()>self.time:
					self.restart()
					break
			if self.heuristic == 0:
				break

n = input("Enter the number of queens you want to play with:")
problem = Hill_climbing(n)
problem.solve()
print(problem.state)