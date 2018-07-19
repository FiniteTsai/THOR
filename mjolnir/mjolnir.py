#!/usr/bin/env python3.6
import numpy as np
import matplotlib.pyplot as plt
import hamarr as ham
import sys
import argparse
import h5py
from imp import reload
reload(ham)

###########################################################################
#
# Options
#
# pview   plot
# uver    Averaged (time and longitude) zonal winds.
#         2D Map Latitude Vs Pressure.
#
# Tver    Averaged (time and longitude) temperatures.
#         2D Map Latitude Vs Pressure.
#
# Tulev   Averaged (time) temperature and wind field.
#         2D Map Longitude Vs Latitude.
#
# PTver   Averaged (time and longitude) potential temperatures.
#         2D Map Latitude Vs Pressure.
#
# ulev    Averaged (time) wind fields in long and lat.
#         2D Map Longitude Vs Latitude.
#
# PVver   Averaged (time and longitude) potential vorticity.
#         2D Map Latitude Vs Pressure.
#
# PVlev   Averaged (time) potential vorticity.
#         2D Map Longitude Vs Latitude.
###########################################################################

parser = argparse.ArgumentParser()
parser.add_argument('pview',metavar='nview',nargs='*',help='Type of plot to make (integer)')
parser.add_argument("-f","--file",nargs=1,default=['results'],help='Results folder to use for plotting')
parser.add_argument("-s","--simulation_ID",nargs=1,default=['Earth'],help='Name of simulation (e.g., planet name)')
parser.add_argument("-i","--initial_file",nargs=1,default=[10],type=int,help='Initial file id number (integer)')
parser.add_argument("-l","--last_file",nargs=1,default=[10],type=int,help='Last file id number (integer)')
parser.add_argument("-p","--pressure_lev",nargs=1,default=[2.5e4],help='Pressure level to plot in temperature/velocity/vorticity field')
parser.add_argument("-pmin","--pressure_min",nargs=1,default=[100],help='Lowest pressure value to plot in vertical plots')
args = parser.parse_args()
pview = args.pview

valid = ['uver','Tver','Tulev','PTver','ulev','PVver','PVlev','vring','pause']
if 'all' in pview:
    pview = valid
else:
    for p in pview:
        if p not in valid:
            raise ValueError('%s not a valid plot option. Valid options are '%p+', '.join(valid))

ntsi     = args.initial_file[0]  # initial file id number
nts      = args.last_file[0]     # last file id number

if ntsi > nts:
    nts = ntsi

simulation_ID = args.simulation_ID[0]
resultsf = args.file[0]

##########
# Planet #
##########

input = ham.input(resultsf,simulation_ID)

########
# Grid #
########

grid = ham.grid(resultsf,simulation_ID)

###############
# Diagnostics #
###############

output = ham.output(resultsf,simulation_ID,ntsi,nts,grid)

#########
# Plots #
#########
# Sigma values for the plotting
sigmaref = np.linspace(input.P_Ref,np.float(args.pressure_min[0]),20)/input.P_Ref

if 'pause' in pview:
    import pdb; pdb.set_trace()
if 'uver' in pview:
    # Averaged zonal winds (latitude vs pressure)
    ham.u(input,grid,output,sigmaref)
if 'Tver' in pview:
    # Averaged temperature (latitude vs pressure)
    ham.temperature(input,grid,output,sigmaref)
if 'Tulev' in pview:
    # Averaged temperature and wind field (longitude vs latitude)
    # PR_LV - Pressure level (Pa)
    PR_LV = np.float(args.pressure_lev[0])
    ham.temperature_u_lev(input,grid,output,PR_LV)
if 'PTver' in pview:
    # Averaged potential temperature (latitude vs pressure)
    ham.potential_temp(input,grid,output,sigmaref)
if 'ulev' in pview:
    PR_LV = np.float(args.pressure_lev[0])
    ham.uv_lev(input,grid,output,PR_LV)
if 'PVlev' in pview:
    PR_LV = np.float(args.pressure_lev[0])
    ham.potential_vort_lev(input,grid,output,PR_LV)
if 'PVver' in pview:
    #sigmaref = np.arange(1,0,-0.05)
    ham.potential_vort_vert(input,grid,output,sigmaref)
#if 'vring' in pview:
    #still in development...
    #sigmaref = np.arange(1,0,-0.05)
    #ham.vring(input,grid,output,sigmaref)