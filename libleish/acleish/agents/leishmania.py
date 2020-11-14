import matplotlib.pyplot as plt
import numpy as np
import random
import csv

from auxiliar_func import *

class Leishmania(object):
    alive = []
    alive_dict = {}

    def __init__(self, coord, spacesize=10, followers=None) -> None:
        """coord = coordinate, followers will track macrophages following it"""
        self.spacesize=spacesize
        self.coord = np.array(coord)
        if followers is None:
            self.followers = []
        self.alive.append(self)

    def move(self) -> None:
        """Leishmania will move when iterated, one step, this place will be
        randomly chosen from its first neighbors """
        self.coord = random.choice(neighborhood(self))
        #return self.coord <------------ Let's see how this works

    def sort(self) -> None:
        """Sort Leishmania.alive into a dict according to the first coordenate of each leish"""
        for i in range(self.spacesize):
            self.alive_dict[i] = [leish for leish in self.alive if leish.coord[0] == i]