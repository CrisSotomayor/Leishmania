import sys
import class_leish as cll
import numpy as np
import random
import time


def simulation(num_leish, num_macro, p, recruit_rate, days=70, steps=96,
                len_infection=28, size=100, draw=False, save=False):
    """Run simulation.

    Parameters:
        num_leish (int): initial leishmania population
        num_macro (int): initial macrophage population
        p (float): probability that leish will infect macrophage following
                   phagocytosis
        recruit_rate (float): percent of initial population of macrophages that
                              get recruited
        days (int): number of days that simulation will run, default is 70 days
                    (10 weeks)
        steps (int): number of "steps" in a day, default is 96 for 15 minute steps
        len_infection (int): days infected before releasing leish
        size (int): space considered will be grid size x size
        draw (bool): default False. If True, draws space at the end of every day.
        save (bool): default False. If true, save graphs and csv with graph data.

        """
    start_time = time.time()
    #Set size as attribute for Leishmania and Macrophage
    cll.Leishmania.spacesize = size
    cll.Macrophage.spacesize = size
    #Emmpty alive lists and dict
    cll.Leishmania.alive = []
    cll.Leishmania.alive_dict = {i:[] for i in range(size)}
    cll.Macrophage.alive = []
    cll.Macrophage.infected = []
    # Data for graphs
    populations = {'Macrophages':[], 'Healthy':[], 'Infected':[], 'Leishmanias':[]}
    # Keep track of recruitment days and if recruitment is active
    recruit_days = 0
    recruitment = False

    # Save initial data for graph
    populations['Time'].append(0)
    populations['Macrophages'].append(num_macro)
    populations['Healthy'].append(num_macro)
    populations['Infected'].append(0) # Initially 0 are infected
    populations['Leishmanias'].append(num_leish)

    iters = int(days*steps) # Iterations the model will perform

    coordinates = []
    for i in range(size):
        for j in range(size):
            coordinates.append((i,j))

    # Create leish and macros, distributed randomly in space
    coor_leish = random.sample(coordinates, num_leish)
    for coor in coor_leish:
        cll.Leishmania(coor)

    coor_macro = random.sample(coordinates, num_macro)
    for coor in coor_macro:
        cll.Macrophage(coor)

    for i in range(iters):
        # Iterate over macros
        for macro in cll.Macrophage.alive:
            macro.time += 1 # Increase time alive or time infected

            if macro.infected == True:
                # If length of infection reached, leish reproduces, else macro moves
                if macro.time == len_infection*steps:
                    macro.Leish_Reproduction()
                    cll.Leishmania.Sort()
                else:
                    macro.Movement_Macro()
            else: # Not infected
                if macro.leish: # If tracking, pursuit
                    macro.Pursuit(p)
                else: # If not tracking, search
                    macro.Search_Leish()
                    if macro.leish: # If now tracking, pursuit
                        macro.Pursuit(p)
                    else:
                        macro.Movement_Macro()

        for leish in cll.Leishmania.alive:
            leish.Movement_Leish()

        cll.Leishmania.Sort() # Sort leish according to new coord

        # If there are more leishmanias than the original amount, assume
        # infection is spreading and begin recruitment
        if len(cll.Leishmania.alive) > num_leish:
            if recruit_days < 7:
                recruitment = True
        # Recruit once each day
        if i%steps == 0 and recruitment == True:
            recruit_days += 1
            cll.Recruitment(coordinates, len(cll.Macrophage.alive), recruit_rate)
        # Stop after a week
        if recruit_days >= 7:
            recruitment = False


        if (i+1)%steps == 0: # Save data at the end of each day (i+1 to save last iteration)
            populations['Time'].append(i+1)
            populations['Macrophages'].append(len(cll.Macrophage.alive))
            populations['Healthy'].append(len(cll.Macrophage.alive) - len(cll.Macrophage.infected))
            populations['Infected'].append(len(cll.Macrophage.infected))
            populations['Leishmanias'].append(len(cll.Leishmania.alive))
            if draw is True:
                cll.DrawSpace()

    # Once simulation is done, create graph, print final amounts and time run
    cll.GraphPopulations(populations, p, recruit_rate, save)
    print('Leishmanias = {}'.format(len(cll.Leishmania.alive)), '\nMacrophages = {}'.format(len(cll.Macrophage.alive)))
    end_time = time.time()
    print(round(end_time-start_time, 2), ' seconds')
