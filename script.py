#!/usr/bin/env python3

import sim_leish
import numpy as np

if __name__ == "__main__":
    
    w_aux = np.arange(0.5, 1, 0.1)
    for w in w_aux:
        sim_leish.simulation(100, 2000, 0.275, 0.21, w, k=1, days=77, 
                             steps=96, len_infection=28, size=350, draw=False, save=True)
            