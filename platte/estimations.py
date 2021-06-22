import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.integrate import quad
import os


def G(Lambda, D=0.04):
    """function for computing G

    Args:
        Lambda (float):
        D (float, optional): should be 0.04 when computing cf
        and -0.96 when computing cw. (Gersten, Herwig, 1992, s.607)
        Defaults to 0.04.

    Returns:
        float: value of G
    """
    def func(G): return Lambda/G + 2*np.log(Lambda/G) - D - Lambda
    return fsolve(func, 0.5)[0]


def cf_unbekannt(Rex):
    g = G(np.log(Rex), 0.04)
    return 2*(0.4/np.log(Rex)*g)**2


def cw_unbekannt(Re):
    g = G(np.log(Re), -0.96)
    return 2*(0.4/np.log(Re)*g)**2


def dy_unbekannt(Re, y_plus, l=1.0):
    return 2 * y_plus * l/Re * (1.0/np.sqrt(cf_unbekannt(Re)/2.0))


def cf_one_seventh(Rex):
    #var = 0.027
    var = 0.02358
    return var/Rex**(1.0/7.0)


def cw_one_seventh(Rex):
    #var = 0.027
    var = 0.02358
    return (7./6.*var)/Rex**(1.0/7.0)


def cf_white(Rex):
    #var = 0.455
    var = 0.4177
    return var*(np.log(0.06*Rex))**(-2.0)


def cf_prandtlKarman(Rex):
    #var = 0.4
    var = 2.12

    try:
        cf = []
        for Rex_ in Rex:
            def func(cf): return 4*np.log10(Rex_*cf**0.5)-cf**(-0.5)-var
            cf.append(fsolve(func, 0.0001)[0])

        return np.array(cf)
    except TypeError:
        def func(cf): return 4*np.log10(Rex*cf**0.5)-cf**(-0.5)-var
        return fsolve(func, 0.0001)[0]


def cf_prandtlSchlichting(Rex):
    #var = 0.455
    var = 0.3596
    return var*(np.log10(Rex)**-2.58)

def cf_blasius_laminar(Rex):
    return 0.664/np.sqrt(Rex)


def cf_experiment():
    df = pd.read_table(os.path.join(
        os.path.dirname(__file__), 'overview.dat'), skipinitialspace=True)
    return df['Re'].values, df['cf'].values


def cw_from_cf(cf_func, Rex1, Rex2):
    integ, _ = quad(cf_func, Rex1, Rex2)
    cw = integ/(Rex2-Rex1)
    return cw


if __name__ == '__main__':

    #print(0.5*dy_unbekannt(1e9, 40)*1e9*(0.5 * cf_unbekannt(1e7))**0.5)
    print(dy_unbekannt(1e7,40.)/dy_unbekannt(5e8,40.))
