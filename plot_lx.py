#!/usr/bin/python3
#
# This script is intended to plot the Lx for a given
# branch. Input parameters are:
# - the branch name
# - the input csv file containing date,


##################################################
#
# requirements
#
##################################################

import pdb
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


##################################################
#
# initialization
#
##################################################

# read year from command line
branch = sys.argv[1]
infile = sys.argv[2]

# initialise list of values
values = []
time_values = []

# open the CSV file
with open(infile, 'r') as csvfile:
    
    # create a csv reader
    csvreader = csv.reader(csvfile)
    
    # Skip the header row if it exists
    next(csvreader, None)
    
    for row in csvreader:
        values.append(float(row[-1]))
        time_values.append(row[0])

# year
year = int(time_values[0].split("-")[0])
        

##################################################
#
# plot
#
##################################################

# build list of ticks
ttt = []
for ddd in range(0, len(time_values)+1, 15):
    ttt.append(time_values[ddd])

# iterate over dates
counter = 0
for d in range(len(values)):
        
    # set x and y            
    x = np.linspace(1,d+1,d+1)
    y = values[0:d+1]
    
    # create a plot
    plt.figure(dpi=300)
    plt.plot(x, y, linewidth=0.8, antialiased=True)
    plt.ylim(0, 20)
    plt.xticks(range(1, 366, 15), ttt, rotation='vertical', fontsize=8)
    plt.yticks(range(0, 30, 5), fontsize=8)
    
    # add labels and title
    plt.xlabel(f"Days of the year {year}", fontsize=10, labelpad=20)
    plt.ylabel('Lx (km)', fontsize=10, labelpad=10)
    plt.title(f"Lx for {branch}")

    # add horizontal lines at y-ticks
    for tick in range(0, 30, 5):
        plt.axhline(y=tick, color='gray', linestyle='--', linewidth=0.3)
    for tick in range(0, 30):
        plt.axhline(y=tick, color='lightgray', linestyle='--', linewidth=0.2, zorder=0)
    
    # save the plot
    print("Saving plot %s" % str(counter))
    plt.tight_layout()
    plt.savefig(f"lx_plot_{counter:04d}.png")
    
    counter += 1 
    
    plt.close('all')
