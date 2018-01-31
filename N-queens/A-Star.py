#!/usr/bin/env python
import numpy as np
import time

class N_queens:
	
	def __init__(self,size):
		self.size = size # size of the board(nxn)
		self.state = [] # state of the system represented by an array (index is column and value stored is row)
		self.heuristic = 0 # no of attacking queens
		self.tempstate = [] # dummy attribute to store simulated position
	
	# Function to randomly assign the initial state of the system
	def random_initial_State(self):
		self.state = np.random.randint(self.size, size=self.size) 
		self.tempstate = np.copy(self.state)

	# Function to calculate the heuristic
	def heuristic_calculator(self):
		self.heuristic=10 # done to make heuristic admissible
		for i in range(len(self.tempstate)):
			for j in range(i+1,len(self.tempstate)):
				if self.tempstate[i]==self.tempstate[j] or np.abs(self.tempstate[i]-self.tempstate[j])==np.abs(i-j):
					self.heuristic+=1
		if(self.heuristic == 10): # if board does not contribute to heuristic set heuristic to 0
			self.heuristic = 0

	# Function to simulate a queen move (to check the heuristic and see if the move is best)
	def moveQueen_simulate(self,Queen_column,direction,steps):
		''' 1-up
		    2-down'''
		self.tempstate = np.copy(self.state) # reset the tempstate to the actual state
		if direction == 1 and self.tempstate[Queen_column]+steps<self.size:
			self.tempstate[Queen_column] += steps
		if direction == 2 and self.tempstate[Queen_column]-steps>=0:
			self.tempstate[Queen_column] -= steps\

	# Function to actually move queen and alter board state
	def moveQueen_actual(self):
		self.state = np.copy(self.tempstate)

class A_star(N_queens):

	def __init__ (self,size):
		N_queens.__init__(self,size)
		self.random_initial_State() # initialize board
		self.heuristic_calculator()	# calculate heuristic
		self.heuristic_min = self.heuristic # to store the value of minimum heuristic
		self.decision = [] # stores the value of column of queen and direction of motion
		self.time = 0 
		
	
if __name__ == '__main__':
	n = int(input("Enter the number of queens you want to play with:"))
	problem = Hill_climbing(n)
	problem.solve_iterate()
	print("The solved state is:")
	print(problem.state)