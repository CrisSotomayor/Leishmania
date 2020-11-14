import numpy as np
import itertools

def neighborhood(agent,r=1,max_rad=3):
    pos = agent.coord
    N = agent.spacesize
    ls = [i for i in itertools.product(range(-max_rad,max_rad+1),range(-max_rad,max_rad+1))]
    crd = {}
    for i in ls:
        try:
            crd[np.max(np.abs(i))].append(i)
        except:
            crd[np.max(np.abs(i))] = [i]
    return list(map(lambda x:[(x[0]+pos[0])%N,(x[1]+pos[1])%N],crd[r]))