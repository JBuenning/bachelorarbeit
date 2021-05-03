import pandas as pd
import numpy as np
import os
from fluidfoam.readpostpro import readforce
from fluidfoam.readof import readmesh
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile as Parser

#plt.rcParams.update({'font.size' : 12})

def get_latest_time(case_dir='.'):
    files = os.listdir(case_dir)
    dirs = [file_ for file_ in files if os.path.isdir(os.path.join(case_dir, file_))]
    times_str = []
    times_float = []
    for dir_ in dirs:
        try:
            time_float = float(dir_)
            times_float.append(time_float)
            times_str.append(dir_)
        except ValueError:
            pass

    latest_time = times_str[np.argmax(times_float)]
    return latest_time

def get_real_wss(case_dir='.', patch='platte'):
    last_timestep = get_latest_time(case_dir)
    wss_parser = Parser(os.path.join(case_dir, last_timestep, 'wallShearStress'))
    wss = np.array(wss_parser['boundaryField'][patch]['value'].val)
    wss_x = wss[:,0]

    try:
        x = np.loadtxt(os.path.join(case_dir, f'{patch}_x_coordinates.csv'))
    except OSError:
        x, y, z = readmesh(case_dir, boundary=patch)
        np.savetxt(os.path.join(case_dir, f'{patch}_x_coordinates.csv'), x)

    return x, wss_x


def get_sampled_wss(case_dir='.'):
    last_timestep = get_latest_time(case_dir)
    df = pd.read_csv(os.path.join(case_dir, 'postProcessing/wallShearStressGraph', last_timestep, 'l1_wallShearStress.csv'))
    x = df['x'].values

    return x, df['wallShearStress_0'].values #only x coordinate


def get_cf(case_dir='.', Re=1e9, l=1.0, return_x=False):

    x, tauw = get_real_wss(case_dir)
    # x, tauw = get_sampled_wss(case_dir)
    cf = tauw * -2.0

    Rex = x * Re / l

    if return_x:
        return x, Rex, cf
    else:
        return Rex, cf

def get_cw_between_Rex(Rex, cf, Rex1, Rex2):

    index1 = np.argmin(np.abs(Rex-Rex1))
    index2 = np.argmin(np.abs(Rex-Rex2))

    Rex = Rex[index1:index2+1]
    Rex[0] = Rex1
    Rex[-1] = Rex2
    cf = cf[index1:index2+1]

    cw = np.trapz(cf, Rex)/(Rex2-Rex1)
    return cw

def get_cw(case_dir):

    forces = readforce(path=case_dir, time_name='latestTime', name='forces')
    viscous_force = forces[-1, 4]
    cw = viscous_force * 20 #mal 10 wegen Bezugsflaeche und Faktor 2 in Formel

    return cw
