#!/usr/bin/env python
# coding: utf-8

# # Class implementation of Leishmania 

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import random
import time
from IPython import display
import seaborn as sns


# In[3]:


class Leishmania(object):
    alive = []
    
    def __init__(self, coord):
        self.coord = np.array(coord)
        Leishmania.alive.append(self)
    
    def Movement_Leish(self):
        """ The Leishmania will move when iterated, one step, this place will be 
        randomly chosen from its first neighbours """
        neighborhood = FirstMooreNeighborhood(self.coord)
        self.coord = random.choice(neighborhood)
        return self.coord
    


# In[5]:


class Macrophage(object):
    alive = [] #keep track of macrophages alive 
    
    def __init__(self, coord, infected, name, time, leish = None):
        """coord = coordinate, infected := True if infected/False if healthy (boolean), 
        name := type of macrophage, time:= time alive/when infected time infected """
        self.coord = np.array(coord)
        self.infected = bool(infected) ##Iniciar como False (?)
        self.name = name
        self.time = int(time)
        if leish is None: 
            self.leish = []    
        Macrophage.alive.append(self)
        
    def print_info(self):
        #prints the information about a macro
        print('Type: {}, Infected: {}, Coordinates: {}, Tiempo: {}, Chasing Leish: {}'
              .format(self.name, self.infected, self.coord, self.time, self.leish))
    
    def Movement_Macro(self):
        """The Macrophage will move when iterated, two steps, 
        this place will be randomly chosen from its second neighbours"""
        neighborhood = SecondMooreNeighborhood(self.coord)
        step = random.choice(neighborhood) 
        self.coord = step
        return self.coord
    
    def Search_Leish(self):
        '''Scan Moore neighborhood with range 3, if Leish found, track it'''
        neighborhood = []
        coord = self.coord
        for i in range(-3,4):
            for j in range(-3,4):
                if i!=0 or j!=0:
                    neighborhood.append(((i+coord[0])%N,(j+coord[1])%N))
        neighborhood = [x for x in vecindad if (x not in FirstMooreNeighborhood(coord))]
        coordinates = [leish.coord for leish in Leishmania.alive]
        #Si crece demasiado el número de leishmanias/macros, puede ser que generar la lista cada vez sea muy poco eficiente
        #Podemos cambiar la función para que se aplique sobre la lista de macros y solo se genere una vez, no sé si Search_Leish(Macrophages.alive) puede estar dentro de la clase
        for n, coor in enumerate(coordinates):
            if coor in neighborhood: #no es realmente al azar la eleccion 
                self.leish = Leishmania.alive[n]    
                return self.leish.coord
            
    def Pursuit(self): 
        '''For Macrophage tracking Leish, take a step towards Leish coordinate '''
        neighborhood = SecondMooreNeighborhood(self.coord)
        min_distance = Distance(self.leish.coord, neighborhood[0])
        closest = neighborhood[0]
        for coor in enumerate(neighborhood): 
            distance = Distance(self.leish.coord, coor)
            if distance < min_distance:
                min_distance = distance
                closest = coor
        #move macrophage
        self.coord = closest
        return self.coord
    
    def Leish_Reproduction(self):
        '''Infected Macrophage dies, releasing new Leish'''
        neighborhood = SecondMooreNeighborhood(self.coord)
        for coor in neighborhood:
            #!!! no existe esto aun 
            ##Leishmania.alive.append(coor)
            ## crear las leishmanias como objetos!
            ##Sin el espacio en sí, aqui podemos meter fácilmente la cantidad de leishmanias, ya no importa si se traslapan 
        #Macrophage dies
        Macrophages.alive.remove(self)
        return
    


# In[1]:


#Neighborhood functions
def FirstMooreNeighborhood(coordinate): 
    '''Moore neighborhood of coordinate with range 1, excluding coordinate '''
    neighborhood = []
    for i in range(-1,2):
        for j in range(-1,2):
            if i!=0 or j!=0:
                neighborhood.append(((i+coordinate[0])%N,(j+coordinate[1])%N))
    return neighborhood


def SecondMooreNeighborhood(coordinate):
    '''Moore neighborhood of coordinate with range 2, excluding neighborhood with range 1'''
    neighborhood = []
    for i in range(-2,3):
        for j in range(-2,3):
            if i!=0 or j!=0:
                neighborhood.append(((i+coordinate[0])%N,(j+coordinate[1])%N))
    neighborhood = [x for x in neighborhood if (x not in FirstMooreNeighborhood(coordinate))]
    return neighborhood


# In[ ]:


#Drawing functions        
def DrawSpace():
    '''Plot Space matrix'''
    Space = np.zeros((size, size))
    for leish in Leishmania.alive:
        (x,y) = leish.coord
        Space[x][y] = 1
    for macro in Macrophages.alive:
        neighborhood = FirstMooreNeighborhood(macro.coord)
        neighborhood.append(macro.coord)
        if macro.infected == False:
            for (x,y) in neighborhood:
                Space[x][y] = 2
        else:
            for (x,y) in neighborhood:
                Space[x][y] = 3
        
    f,ax = plt.subplots(1,1,figsize=(3,3),dpi=120)
    ax.imshow(Space,vmin=0,vmax = 3,cmap='jet')
    plt.show()
    plt.close()
    
    return Space


# In[ ]:


#Other functions
def Distance(a,b):
    '''Distance from a to b, rounded to 1 decimal'''
    dist = ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)
    return round(dist,1)


# In[ ]:


class Leuco(Macrophage):
    pass


# Notas:
# <ol>
#     <li>regresar error si algo no se puede (ej. pedir leish_reproduction a un macro no infectado)
#     <li>no sé cómo usar las listas de leish/macro, parece mala idea usarlas en las clases si las listas se definen fuera de ellas, no sé qué tan bien es definirlas dentro de las clases (weakrefs?) 
#     <li>donde meter info sobre días/cuantas iteraciones hacen un día
#     <li>que macrophages y leishmania sean subclases? que la clase principal sea como 'agents' o algo, puede facilitar llevar la cuenta de las coordenadas dentro de las clases
#     <li>se puede obtener lista de coord facilmente? Algo como [i.coord for i in Macrophage.alive]? Sí, eso sirve
                #si lo corres muchas veces, se guardan cosas repetidas, hay que vaciar la lista cuando corramos más simulaciones
#       #en el tiempo, llevaremos la cuenta al moverlo? o definimos una función que sea como "iterar" y lo cambiamos ahi?

 #<ol/>
#         
#         
# Por definir:
# <ol>
#     <li>def initial_population 
         # size (tamaño inicial )
#     <li>coordinates
#    
# <ol/>

# In[ ]:




