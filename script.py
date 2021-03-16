#!/usr/bin/env python3

import sim_leish
import numpy as np

if __name__ == "__main__":
    
    pro = np.arange(0.2, 0.4, 0.025)
    rec = np.arange(0.2, 0.5, 0.025)
    for p in pro:
        for r in rec:
            sim_leish.simulation(100, 2000, p, r, days=77, steps=96,
                len_infection=28, size=350, draw=False, save=True)
            