import matplotlib.pyplot as plt
from datetime import datetime
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


#Neighborhood functions
def FirstMooreNeighborhood(agent):
    '''Moore neighborhood of object with range 1, excluding coordinate '''
    neighborhood = []
    coordinate = agent.coord
    N = agent.spacesize
    for i in range(-1,2):
        for j in range(-1,2):
            if i!=0 or j!=0:
                neighborhood.append(np.array(((i+coordinate[0])%N,(j+coordinate[1])%N)))
    return neighborhood


def SecondMooreNeighborhood(agent):
    '''Moore neighborhood of coordinate with range 2, excluding neighborhood with range 1'''
    coordinate = agent.coord
    N = agent.spacesize
    auxi = [[-2,-2],[-2,-1],[-2,0],[-2,1],[-2,2], # improve this
            [-1,-2],[-1,2],[0,-2],[0,2],[1,-2],[1,2],
            [2,-2],[2,-1],[2,0],[2,1],[2, 2]]
    neighborhood = [np.array(np.array(((i[0]+coordinate[0])%N,(i[1]+coordinate[1])%N))) for i in auxi]

    return neighborhood

def ThirdMooreNeighborhood(agent):
    '''Moore neighborhood of coordinate with range 3, excluding neighborhood with range 2'''
    coordinate = agent.coord
    N = agent.spacesize
    auxi = [[3,-2],[3,-1],[3,1],[3,0],[3,-3],[3,3],[0,3],[0,-3],[1,3],[1,-3],
             [-1,-3],[2,-3],[2,3],[-3,-3],[-3,3],[-3,2],[3,2],[-2,3],[-1,3],[-3,0],
             [-3,1],[-3,-1],[-3,-2],[-2,-3]]
    neighborhood = [np.array(np.array(((i[0]+coordinate[0])%N,(i[1]+coordinate[1])%N))) for i in auxi]

    return neighborhood


#Other functions
def Recruitment(coordinates, current_population, recruit_rate):
    '''Create new macrophages, creates recruit_rate percentage of current population'''
    new_macros = int(current_population*recruit_rate)
    new_coords = random.choices(coordinates, k=new_macros)

    for coor in new_coords:
        Macrophage(coor)
    return


def DrawSpace():
    """Plot Space matrix. """
    size = Macrophage.spacesize

    Space = np.zeros((size, size))
    for leish in Leishmania.alive:
        x = leish.coord[0]
        y = leish.coord[1]
        Space[x][y] = 1
    for macro in Macrophage.alive:
        neighborhood = FirstMooreNeighborhood(macro)
        neighborhood.append(macro.coord)
        if macro.infected == False:
            for co in neighborhood:
                Space[co[0]][co[1]] = 2
        else:
            for co in neighborhood:
                Space[co[0]][co[1]] = 3

    f,ax = plt.subplots(1,1,figsize=(3,3),dpi=120)
    ax.imshow(Space,vmin=0,vmax = 3,cmap='jet')
    plt.show()
    plt.close()

    return Space


def GraphPopulations(populations, p, recruit_rate, save):
    """Draw graph showing population evolution, if save, saves graph and csv. """
    fig1 = plt.figure()
    plt.title(f"Population Evolution (p = {p}, r={recruit_rate})")
    plt.ylabel('Population')
    plt.xlabel('Days')

    t = np.linspace(0, len(populations['Leishmanias']) - 1, len(populations['Leishmanias']))

    plt.plot(t, populations['Leishmanias'], label = 'Leishmanias')
    plt.plot(t, populations['Macrophages'], label = 'Macrophages')
    plt.legend(loc = 'upper left')


    fig2 = plt.figure()
    plt.title(f"Macrohage Populations Evolution (p = {p}, r={recruit_rate})")
    plt.ylabel('Population')
    plt.xlabel('Days')

    t_aux = np.linspace(0, len(populations['Macrophages']) - 1, len(populations['Macrophages']))

    plt.plot(t_aux, populations['Healthy'], label = 'Healthy')
    plt.plot(t_aux, populations['Infected'], label = 'Infected')
    fig2.legend(loc = 'upper left') 

    now = datetime.now()
    dtstring = now.strftime("%f")
    
    if save:
        fig1.savefig(f"p{p}r{recruit_rate}_{dtstring}.png")
        fig2.savefig(f"macro_p{p}r{recruit_rate}_{dtstring}.png")
        with open(f"p{p}r{recruit_rate}_{dtstring}.csv", "w", newline='') as outfile:
           writer = csv.writer(outfile)
           writer.writerow(populations.keys())
           writer.writerows(zip(*populations.values()))

    fig1.show()
    fig2.show()
    plt.close()

    return None


def Distance(a,b):
    '''Distance from a to b, rounded to 1 decimal'''
    dist = ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)
    return round(dist,1)
