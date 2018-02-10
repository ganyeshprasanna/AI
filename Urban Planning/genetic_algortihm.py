# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 01:14:33 2018

@author: Ganesh
"""

import numpy as np
from sympy.utilities.iterables import multiset_permutations

class Map:
    def __init__(self,input):
        self.given_map = []
        self.input = input
        self.industry = 0
        self.residential = 0
        self.commercial = 0

    def get_map(self):
        with open(self.input) as f:
    # whenever \n is encountered splitlines will break and take the encountered part aas a string
            my_list = f.read().splitlines()

#my_list = [x.strip() for x in my_list.split(',')]
        self.industry = int(my_list[0])
        self.residential = int(my_list[1])
        self.commercial = int(my_list[2])
        for i in range(3):
            del my_list[0]

        for i in range(len(my_list)):
            self.given_map.append(my_list[i].split(','))

        for i in range(len(self.given_map)):
            for j in range(len(self.given_map[0])):
                if self.given_map[i][j].isdigit():
                    self.given_map[i][j] = int(self.given_map[i][j])
                elif self.given_map[i][j] == 'X':
                    self.given_map[i][j] = 10
                elif self.given_map[i][j] == 'S':
                    self.given_map[i][j] = 11

# coverting into array
        self.given_map = np.array(self.given_map)

class Environment(Map):
    def __init__(self,input):
        Map.__init__(self,input)
        self.get_map()
        self.score = 0
        self.manhattan_check_non_res = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1],
                                [1, 0], [1, 1], [0, -2], [0, 2], [2, 0], [-2, 0]])
        self.manhattan_check_res = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1],
                                [1, 0], [1, 1], [0, -2], [0, 2], [2, 0], [-2, 0]])
        self.i_indices = []
        self.r_indices = []
        self.c_indices = []
        
    def get_score(self,my_map):
        x_indices = np.asarray(np.where(self.given_map == 10)).T
        s_indices = np.asarray(np.where(self.given_map == 11)).T
        i_indices = np.asarray(np.where(my_map == 12)).T
        r_indices = np.asarray(np.where(my_map == 13)).T
        c_indices = np.asarray(np.where(my_map == 14)).T

        for indices in x_indices:
            x_neighbours = self.manhattan_check_non_res + indices
            x_neighbours = (x_neighbours.T[:,x_neighbours.T.min(axis=0)>=0]).T
            x_neighbours = (x_neighbours.T[:,x_neighbours.T.min(axis=0)>=0]).T
            for i,j in x_neighbours:
                try:
                    if my_map[i,j] == 12:
                        self.score -= 10
                    if my_map[i,j] == 13 or my_map[i,j] == 14:
                        self.score -=20
                except IndexError:
                    pass

        for indices in s_indices:
            s_neighbours = self.manhattan_check_non_res + indices
            s_neighbours = (s_neighbours.T[:,s_neighbours.T.min(axis=0)>=0]).T
            for i,j in s_neighbours:
                try:
                    if my_map[i,j] == 13:
                        self.score += 10
                except IndexError:
                    pass

        for indices in i_indices:
            i_neighbours = self.manhattan_check_non_res + indices
            i_neighbours = (i_neighbours.T[:,i_neighbours.T.min(axis=0)>=0]).T    
            for i,j in i_neighbours:
                try:
                    if my_map[i,j] == 12:
                        self.score += 3
                    if self.given_map[i,j] !=11:
                        self.score -= self.given_map[i,j]
                except IndexError:
                    pass

        for indices in c_indices:
            c_neighbours = self.manhattan_check_non_res + indices
            c_neighbours = (c_neighbours.T[:,c_neighbours.T.min(axis=0)>=0]).T    
            for i,j in c_neighbours:
                try:
                    if my_map[i,j] == 14:
                        self.score -= 5
                    if self.given_map[i,j] !=11:
                        self.score -= self.given_map[i,j]
                except IndexError:
                    pass

        for indices in r_indices:
            r_neighbours = self.manhattan_check_res + indices
            r_neighbours = (r_neighbours.T[:,r_neighbours.T.min(axis=0)>=0]).T    
            for i,j in c_neighbours:
                try:    
                    if my_map[i,j] == 12:
                        self.score -= 5
                    if my_map[i,j] == 14:
                        self.score += 5
                    if self.given_map[i,j] !=11:
                        self.score -= self.given_map[i,j]
                except IndexError:
                    pass

class Genetic_Algortithm(Environment):
    def __init__(self,input):
        Environment.__init__(self,input)
        self.size = 100
        self.my_map = []
        self.population = []

    def initialize_map(self):
        self.my_map = np.zeros(self.given_map.shape).flatten()
        self.my_map[0:self.industry] = 12
        self.my_map[self.industry:self.residential+self.industry] = 13
        self.my_map[self.residential+self.industry:self.residential+self.industry+self.commercial] = 14

    def populate(self):
        i=0
        for pops in multiset_permutations(self.my_map):
            a = np.array(pops).reshape(self.given_map.shape)
            b_1 = a==12
            b_2 = a==13
            b_3 = a==14
            if 10 not in self.given_map[b_1] and 10 not in self.given_map[b_2] and 10 not in self.given_map[b_3]:
                self.population.append(a)
                i += 1
            if i == 100:
                break