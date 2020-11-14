import matplotlib.pyplot as plt
import numpy as np
import random
import csv

class Macrophage(object):
    alive = [] # Keep track of alive macrophages
    infected = [] # Keep track of infected macrophages

    def __init__(self, coord, infected=False, name=None, time=0, leish=None):
        """coord = coordinate, infected := True if infected/False if healthy (boolean),
        name := type of macrophage, time:= time alive/time infected """
        self.coord = np.array(coord)
        Macrophage.alive.append(self)
        self.infected = infected
        self.time = time
        self.leish = leish

    def print_info(self):
        """"Prints macrophage information. """
        print(f'Type: {self.name}, Infected: {self.infected},'
              f'Coordinates: {self.coord}, Time: {self.time},'
              f'Chasing Leish: {self.leish}')

    def Movement_Macro(self):
        """The Macrophage will move when iterated, two steps,
        this place will be randomly chosen from its second neighbors"""
        neighborhood = SecondMooreNeighborhood(self)
        step = random.choice(neighborhood)
        self.coord = step
        return self.coord

    def Search_Leish(self):
        """Scan Moore neighborhood with range 3, if Leish found, track it"""
        neighborhood = ThirdMooreNeighborhood(self)
        coord = self.coord
        N = self.spacesize

        # Get third Moore neighborhood, exclude own coordinate

        # To reduce running time, look only in corresponding Moore neighborhood cols
        interval = [(coord[0]+i)%N for i in range(-3,4)]
        for i in interval:
            for leish in Leishmania.alive_dict[i]:
                if any(np.array_equal(leish.coord, x) for x in neighborhood):
                    self.leish = leish
                    self.leish.followers.append(self)
                    return

    def Chase(self):
        """Take a step towards Leish being chased. """
        neighborhood = SecondMooreNeighborhood(self)
        min_distance = Distance(self.leish.coord, neighborhood[0])
        closest = neighborhood[0]
        for coor in neighborhood:
            distance = Distance(self.leish.coord, coor)
            if distance < min_distance:
                min_distance = distance
                closest = coor
        return closest

    def Pursuit(self, p):
        '''For Macrophage tracking Leish, take a step towards Leish coordinate.
        If Leish is reached, macrophage gets infected with probability p. '''

        self.coord = self.Chase() # Move macrophage
        # If leish in self.coord or first Moore neighborhood, phagocyte it
        search_area = FirstMooreNeighborhood(self)
        search_area.append(self.coord)
        if any(np.array_equal(self.leish.coord, x) for x in search_area):
            leish_to_delete = self.leish # Store leish to be deleted
            # Alert followers of death, followers stop tracking it
            for macro in self.leish.followers:
                macro.leish = None
            # Remove from alive list and dict
            Leishmania.alive.remove(leish_to_delete)
            Leishmania.alive_dict[leish_to_delete.coord[0]].remove(leish_to_delete)

            if random.random() < p: # Infected with probability p
                self.infected = True
                Macrophage.infected.append(self)
                self.time = 0
        return self.coord

    def Leish_Reproduction(self):
        '''Infected Macrophage dies, releasing new Leish'''
        neighborhood = SecondMooreNeighborhood(self) + ThirdMooreNeighborhood(self)
        for coor in neighborhood:
            Leishmania(coor)
        Macrophage.alive.remove(self)
        Macrophage.infected.remove(self)
        return