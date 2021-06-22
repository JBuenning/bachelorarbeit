from bachelorarbeit.platte.get_data import get_cf, get_cw, get_cw_between_Rex
from bachelorarbeit.platte.estimations import *
import matplotlib.pyplot as plt
import os
import re
import numpy as np
#plt.rcParams.update({'font.size' : 14})



def compare_cf(var_name, dir='.', ax=plt, exclude=[], exchange_names={'kOmega':r'$k-\omega$',
                                                                'kEpsilon':r'$k-\epsilon$',
                                                                'kOmegaSST':r'$k-\omega SST$'}):

    dirs = [file_ for file_ in os.listdir(dir) if os.path.isdir(os.path.join(dir, file_))]

    if var_name:
        dirs.sort(key=lambda f: float(re.findall(r"[-+]?\d*\.\d+|\d+", f)[-1]))
    else:
        dirs.sort()
    

    for file_ in dirs:
        
        if var_name:
            var = float(re.findall(r"[-+]?\d*\.\d+|\d+", file_)[-1])
        else:
            if file_ in exchange_names:
                var = exchange_names[file_]
            else:
                var = file_
        if file_ in exclude or var in exclude:
            continue

        Rex, cf = get_cf(os.path.join(dir, file_))

        if var_name:
            ax.scatter(Rex, cf, label=f'{var_name} {var}')
        else:
            ax.scatter(Rex, cf, label=f'{var}')


def compare_cf_analytical(Rex=np.sort(np.concatenate((np.geomspace(1e5, 1e10, 1000),
            np.linspace(1e5, 1e10, 1000)))), ax=plt):
    #fuer log und lineare Verteilung
    # Rex = np.sort(np.concatenate((np.geomspace(1e5, 1e9, 1000),
    #             np.linspace(1e5, 1e9, 1000))))

    # cf = list(map(cf_unbekannt, Rex))
    # ax.plot(Rex, cf, color='black', label=r'$c_f = 2(\frac{\kappa}{\ln Re} \mathrm{G}(\Lambda; D))^2$')
    cf = cf_one_seventh(Rex)
    ax.plot(Rex, cf, label='1/7th law', zorder=100)
    cf = cf_white(Rex)
    ax.plot(Rex, cf, label='White', zorder=100)
    cf = cf_prandtlKarman(Rex)
    ax.plot(Rex, cf, label='Prandtl-Kármán', zorder=100)
    cf = cf_prandtlSchlichting(Rex)
    ax.plot(Rex, cf, label='Prandtl-Schlichting', zorder=100)
    # cf = cf_blasius_laminar(Rex)
    # ax.plot(Rex, cf, label='Blasius (laminar)', zorder=100)

    Rex, cf = cf_experiment()
    ax.scatter(Rex, cf, label='Experimentell nach Osterlund',
                marker='x', color='black', s=60, zorder=99)


def compare_cw_over_Rex(var_name, dir='.', ax=plt, exclude=[], exchange_names={'kOmega':r'$k-\omega$',
                                                                'kEpsilon':r'$k-\epsilon$',
                                                                'kOmegaSST':r'$k-\omega SST$'}):

    dirs = [file_ for file_ in os.listdir(dir) if os.path.isdir(os.path.join(dir, file_))]

    if var_name:
        dirs.sort(key=lambda f: float(re.findall(r"[-+]?\d*\.\d+|\d+", f)[-1]))
    else:
        dirs.sort()
    

    for file_ in dirs:
        
        if var_name:
            var = float(re.findall(r"[-+]?\d*\.\d+|\d+", file_)[-1])
        else:
            if file_ in exchange_names:
                var = exchange_names[file_]
            else:
                var = file_
        if file_ in exclude or var in exclude:
            continue

        Rex_plate, cf_plate = get_cf(os.path.join(dir, file_))
        Rex = np.sort(np.concatenate((np.geomspace(5e5, 1e10, 100),
                np.linspace(5e5, 1e10, 100))))

        cw = [get_cw_between_Rex(Rex_plate, cf_plate, Rex[0], Rex_) for Rex_ in Rex]

        if var_name:
            ax.scatter(Rex, cw, label=f'{var_name} {var}')
        else:
            ax.scatter(Rex, cw, label=f'{var}')

def compare_cw_over_Rex_analytical(Rex=np.sort(np.concatenate((np.geomspace(5e5, 1e10, 1000),
                np.linspace(5e5, 1e10, 1000)))), ax=plt):

    cw = [cw_from_cf(cf_one_seventh, Rex[0], Rex_) for Rex_ in Rex]
    ax.plot(Rex, cw, label='1/7th law')
    cw = [cw_from_cf(cf_white, Rex[0], Rex_) for Rex_ in Rex]
    ax.plot(Rex, cw, label='White')
    # cw = [cw_from_cf(cf_prandtlKarman, Rex[0], Rex_) for Rex_ in Rex]
    # ax.plot(Rex, cw, label='Prandtl-Kármán')
    cw = [cw_from_cf(cf_prandtlSchlichting, Rex[0], Rex_) for Rex_ in Rex]
    ax.plot(Rex, cw, label='Prandtl-Schlichting')
    cw = 0.075/(np.log10(Rex)-2)**2
    plt.plot(Rex, cw, label = 'ITTC-57')
    # cw = [cw_from_cf(cf_blasius_laminar, Rex[0], Rex_) for Rex_ in Rex]
    # ax.plot(Rex, cw, label='Blasius (laminar)')


def compare_cw(var_name, dir='.', interval_pct=False, interval_index=-1, analytic=False, exchange_names={'kOmega':r'$k-\omega$',
                                                                                                        'kEpsilon':r'$k-\epsilon$',
                                                                                                          'kOmegaSST':r'$k-\omega SST$'}):

    vars_ = []
    cws = []
    #cws_ich = []

    dirs = [file_ for file_ in os.listdir(dir) if os.path.isdir(os.path.join(dir, file_))]
    if var_name:
        dirs.sort(key=lambda f: float(re.findall(r"[-+]?\d*\.\d+|\d+", f)[-1]))
    else:
        dirs.sort()


    for file_ in dirs:

        if var_name:
            var = float(re.findall(r"[-+]?\d*\.\d+|\d+", file_)[-1])
        else:
            if file_ in exchange_names:
                var = exchange_names[file_]
            else:
                var = file_

        cw = get_cw(os.path.join(dir, file_))
        vars_.append(var)
        cws.append(cw)

        # Rex, cf = get_cf(file_)
        # Rex = list(Rex)
        # cf = list(cf)
        # Rex.insert(0, 0.0)
        # cf.insert(0, cf[0])
        # Rex.append(1e9)
        # cf.append(cf[-1])
        # cws_ich.append(np.trapz(cf, Rex)/1e9)


    if interval_pct and var_name:
        y1 = cws[interval_index] * (1 + interval_pct/100.0)
        y2 = cws[interval_index] * (1 - interval_pct/100.0)

        plt.fill_between([max(vars_), min(vars_)], y1, y2, alpha=0.25, label=rf'$\pm${interval_pct}% Abweichung')
        plt.legend()

    plt.grid()
    if var_name:
        plt.scatter(vars_, cws, marker='x', color='black')
        # plt.scatter(vars_, cws_ich, label='Integral ueber $c_f$')
        #plt.legend()
        plt.xlabel(var_name)
        if analytic:
            cw = cw_unbekannt(1e10)
            plt.plot([min(vars_), max(vars_)], [cw, cw], color='black', label=r'$c_w = 2(\frac{\kappa}{\ln Re} \mathrm{G}(\Lambda; D))^2$')
            plt.legend()
    else:
        if analytic:
            vars_.append(r'$c_w = 2(\frac{\kappa}{\ln Re} \mathrm{G}(\Lambda; D))^2$')
            cws.append(cw_unbekannt(1e10))
        plt.bar(vars_, cws)
    plt.ylabel(r'$c_{W \nu}$')
    #plt.tight_layout()
    plt.show()

