#!/usr/bin/env python
#import time
from queue import PriorityQueue
import random
from itertools import count
#from timeit import default_timer as timer
#import numpy as np
import time

tie = count() #global

class N_queens:

	def __init__(self,size):
		self.size = size # size of the board(nxn)
		self.state = {} # state of the system represented by an array (index is column and value stored is row)
		self.heuristic = 0 # no of attacking queens
		self.tempstate = {} # dummy attribute to store simulated position

	# Function to randomly assign the initial state of the system
	def random_initial_State(self):
		self.state = {x: random.randint(0,self.size-1)  for x in range(self.size)}
		self.tempstate = dict(self.state)

	# Function to calculate the heuristic
	def heuristic_calculator(self):
		self.heuristic=10 # done to make heuristic admissible
		for i in range(self.size):
			for j in range(i+1,self.size):
				if self.tempstate[i]==self.tempstate[j] or abs(self.tempstate[i]-self.tempstate[j])==abs(i-j):
					self.heuristic+=1
		if(self.heuristic == 10): # if board does not contribute to heuristic set heuristic to 0
			self.heuristic = 0

	# Function to simulate a queen move (to check the heuristic and see if the move is best)
	def moveQueen_simulate(self,Queen_column,direction,steps):
		''' 1-up
		    2-down'''
		self.tempstate = dict(self.state) # reset the tempstate to the actual state
		if direction == 1 and self.tempstate[Queen_column]+steps<self.size:
			self.tempstate[Queen_column] += steps
			return True
		elif direction == 2 and self.tempstate[Queen_column]-steps>=0:
			self.tempstate[Queen_column] -= steps
			return True
		else:
			return False

	# Function to actually move queen and alter board state
	def moveQueen_actual(self):
		self.state = dict(self.tempstate)

class A_star(N_queens):

	def __init__ (self,size):
		N_queens.__init__(self,size)
		self.random_initial_State() # initialize board
		self.initial_state = dict(self.state)
		self.heuristic_calculator()	# calculate heuristic
		#self.heuristic_min = self.heuristic # to store the value of minimum heuristic
		self.decision = [] # stores the value of column of queen and direction of motion
		self.time = time.time()
		self.explored = PriorityQueue(0)
		self.cost = 0
		self.total = self.heuristic
		self.a = list(range(self.size))
		self.expand = []
		self.nodes_expanded = 1
		self.depth = 1

	def cost_calculator(self):
		self.cost = self.total - self.heuristic

	def total_calculator(self,steps):
		self.total = self.cost + self.heuristic + (steps**2) + 10

	def solver(self):
	 	#self.time = time.time() + 10
		while self.heuristic>0:
			#self.heuristic_calculator()
			#print(self.heuristic)
			self.cost_calculator()
			#print("hey")
			#self.decision = []
			for i in self.a:
				for j in [1,2]:
					for k in range(1,self.size):
						#print(self.tempstate,self.state)
						if self.moveQueen_simulate(i,j,k):
							#print(self.tempstate)
							#print(self.cost)
							self.heuristic_calculator()
							#print(self.heuristic)
							self.total_calculator(k)
							#print(self.total)
							#print([self.total,self.tempstate])
							self.explored.put([self.total,next(tie),self.tempstate,i,self.depth])
							#print('yo')
			
			if not self.explored.empty():
				#print('hi')
				self.nodes_expanded += 1
				self.expand = self.explored.get()
				#print(self.tempstate)
				self.state = dict(self.expand[2]);self.total = self.expand[0]
				self.depth = self.expand[4] + 1
				self.tempstate = dict(self.state)
				#print(self.state)
				#print(self.total)
				self.heuristic_calculator()
				#print(self.heuristic)
				self.a = list(range(self.size))
				self.a.remove(self.expand[3])

			if self.heuristic == 0:
				print("Solved")
				self.time = (time.time()-self.time)
				break

				#print(self.heuristic)
			'''if time.time()>self.time or not self.decision:
				print('yo')
				self.decision=[]
				self.restart()
				break
			if self.heuristic == 0:
				print("Solved")
				break
		if self.heuristic == 0:
			print("Solved")
			print("The solved state is:")
			print(problem.state)
			break'''
def main():
	m = int(input("Enter the number of queens you what to work with:"))
	if m>3:
		problem=A_star(m)
		print("The initial state of the board is:")
		print(problem.state)
		print("The state is represented by a dictionary. The keys correspond to the column of the board and the value stored is the row in which the queen is placed.")
		problem.solver()
		print("The solved state of the board is:")
		print(problem.tempstate)
		print("The cost to move is:")
		print(problem.total)
		print("Number of nodes expanded", problem.nodes_expanded)
		print("Effective branching factor is", problem.nodes_expanded/problem.depth)
		print("Time elapsed",problem.time)
	else:
		print("Can't Solve for number of queens =",m)
	return problem.nodes_expanded

if __name__ == "__main__":
	a=main()