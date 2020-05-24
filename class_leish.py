import matplotlib.pyplot as plt
import numpy as np
import random


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
        neighborhood = []
        coord = self.coord
        N = self.spacesize

        # Get third Moore neighborhood, exclude own coordinate
        for i in range(-3,4):
            for j in range(-3,4):
                if i!=0 or j!=0:
                    neighborhood.append(np.array(((i+coord[0])%N,(j+coord[1])%N)))

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
        neighborhood = SecondMooreNeighborhood(self)
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

#Other functions
def Recruitment(coordinates, num_macro, recruit_rate):
    '''Create new macrophages, creates recruit_rate percentage of original population'''
    new_macros = int(num_macro*recruit_rate)
    new_coords = random.sample(coordinates, new_macros)

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


def GraphPopulations(populations, p, num_leish, num_macro):
    plt.figure()
    plt.title('Population Evolution (p = {}, M = {}, L = {})'.format(p, populations['Macrophages'][0],
                                                                        populations['Leishmanias'][0]))
    plt.ylabel('Population')
    plt.xlabel('Days')

    t = np.linspace(0, len(populations['Leishmanias']) - 1, len(populations['Leishmanias']))

    plt.plot(t, populations['Leishmanias'], label = 'Leishmanias')
    plt.plot(t, populations['Healthy'], label = 'Healthy')
    plt.plot(t, populations['Infected'], label = 'Infected')
    plt.plot(t, populations['Macrophages'], label = 'Macrophages')
    plt.legend(loc = 'upper left')

    #plt.savefig('p'+ str(p) + 'M'+ str(num_macro)+ 'L'+ str(num_leish)+ '.png')
    plt.show()
    plt.close()

    return None


def Distance(a,b):
    '''Distance from a to b, rounded to 1 decimal'''
    dist = ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)
    return round(dist,1)
