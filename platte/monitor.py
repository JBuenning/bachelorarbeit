import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["toolbar"] = "toolmanager"
from matplotlib.backend_tools import ToolToggleBase
from fluidfoam.readpostpro import readforce
import time
import warnings
warnings.filterwarnings('ignore')


def monitor():

    path = ''

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, sharex='col')

    start_times = os.listdir(os.path.join(path, 'postProcessing/residuals'))
    indiv_res = []
    for start_time in start_times:
        indiv_res.append(pd.read_table(os.path.join(path, 'postProcessing/residuals', start_time, 'residuals.dat'), skiprows=1))

    residuals = pd.concat(indiv_res, ignore_index=True)
    residuals = residuals.dropna()
    residuals.columns = residuals.columns.str.replace(r'[ #]', '')

    indiv_forces = []
    for start_time in start_times:
        indiv_forces.append(readforce(path=path, time_name=start_time, name='forces'))

    forces = np.concatenate(tuple(indiv_forces))

    viscous_force = forces[:, 4]*20 #mal 10 wegen Bezugsflaeche und Faktor 2 in Formel
    time_force = forces[:, 0]

    ax1.set_yscale('log')
    ax1.grid()
    ax1.set_ylabel('Residuum')

    ax2.grid()
    ax2.set_xlabel('Iterationsschritt')
    ax2.set_ylabel('$c_W$')

    line1_1, = ax1.plot(residuals['Time'], residuals['Ux'], label='Residuum $U_x$')
    line1_2, = ax1.plot(residuals['Time'], residuals['Uy'], label='Residuum $U_y$')
    line1_3, = ax1.plot(residuals['Time'], residuals['p'], label='Residuum $p$')
    line1_4, = ax1.plot(residuals['Time'], residuals['k'], label='Residuum $k$')
    if 'epsilon' in residuals:
        line1_5, = ax1.plot(residuals['Time'], residuals['epsilon'], label='Residuum $\epsilon$')
    if 'omega' in residuals:
        line1_6, = ax1.plot(residuals['Time'], residuals['omega'], label='Residuum $\omega$')


    line2_1, = ax2.plot(time_force, viscous_force, label=r'$c_{W,\nu}$', color='black', linestyle='None', marker='o', markersize=2.0)

    fig.legend(loc='upper right')

    tm = fig.canvas.manager.toolmanager
    tm.add_tool("autorescale", ToolToggleBase)
    tm.get_tool("autorescale").enable()
    fig.canvas.manager.toolbar.add_tool(tm.get_tool("autorescale"), "toolgroup")
    tm.trigger_tool(name='autorescale')

    while True:

        start_times = os.listdir(os.path.join(path, 'postProcessing/residuals'))
        indiv_res = []
        for start_time in start_times:
            indiv_res.append(pd.read_table(os.path.join(path, 'postProcessing/residuals', start_time, 'residuals.dat'), skiprows=1))

        residuals = pd.concat(indiv_res, ignore_index=True)
        residuals = residuals.dropna()
        residuals.columns = residuals.columns.str.replace(r'[ #]', '')

        indiv_forces = []
        for start_time in start_times:
            indiv_forces.append(readforce(path=path, time_name=start_time, name='forces'))

        forces = np.concatenate(tuple(indiv_forces))
        viscous_force = forces[:, 4]*20 #mal 10 wegen Bezugsflaeche und Faktor 2 in Formel
        time_force = forces[:, 0]

        line1_1.set_data(residuals['Time'], residuals['Ux'])
        line1_2.set_data(residuals['Time'], residuals['Uy'])
        line1_3.set_data(residuals['Time'], residuals['p'])
        line1_4.set_data(residuals['Time'], residuals['k'])
        if 'epsilon' in residuals:
            line1_5.set_data(residuals['Time'], residuals['epsilon'])
        if 'omega' in residuals:
            line1_6.set_data(residuals['Time'], residuals['omega'])

        line2_1.set_data(time_force, viscous_force)

        fig.canvas.draw()

        ax1.relim()
        ax2.relim()
        
        if tm.get_tool('autorescale').toggled:
            ax1.autoscale_view(tight=False)
            ax2.autoscale_view(tight=False)

        fig.canvas.flush_events()
        plt.pause(5)
