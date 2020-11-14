import matplotlib.pyplot as plt
import numpy as np
import random
import csv


class Leishmania(object):
    alive = []
    alive_dict = dict()
    #spacesize = 10

    def __init__(self, coord, followers=None):
        """coord = coordinate, followers will track macrophages following it"""
        self.coord = np.array(coord)
        if followers is None:
            self.followers = []

        Leishmania.alive.append(self)

    def Movement_Leish(self):
        """Leishmania will move when iterated, one step, this place will be
        randomly chosen from its first neighbors """
        neighborhood = FirstMooreNeighborhood(self)
        self.coord = random.choice(neighborhood)
        return self.coord

    def Sort():
        """Sort Leishmania.alive into a dict according to the first coordenate of each leish"""
        for i in range(Leishmania.spacesize):
            Leishmania.alive_dict[i] = [leish for leish in Leishmania.alive if leish.coord[0] == i]
        return