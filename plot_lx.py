#!/usr/bin/python3
#
# This script is intended to plot the Lx for a given
# branch. Input parameters are:
# - the branch name
# - the input csv file for Lx
# - the output directory

##################################################
#
# requirements
#
##################################################

import os
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
outdir = sys.argv[3]
    
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
ticks = []
ticks_indices = []

counter = 0
for date_string in time_values:

    # create a date object from the current date
    date_object = datetime.strptime(date_string, "%Y-%m-%d")

    # if day == 1 or 15, we add it to the ticks
    if date_object.day == 15 or date_object.day == 1:
        ticks.append(date_string)
        ticks_indices.append(counter)

    # increment counter
    counter += 1

# add the last day of the year to the ticks
ticks.append(time_values[-1])
ticks_indices.append(counter-1)

# iterate over dates to plot images
counter = 0
for d in range(len(values)):
        
    # set x and y            
    x = np.linspace(1,d+1,d+1)
    y = values[0:d+1]
    
    # create a plot
    plt.figure(dpi=300)
    plt.plot(x, y, linewidth=0.8, antialiased=True)
    plt.ylim(0, 20)
    plt.xticks(ticks_indices, ticks, rotation='vertical', fontsize=8)
    plt.yticks(range(0, 30, 5), fontsize=8)

    # set fixed limit
    plt.xlim(1, len(time_values)+10)
    
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
    outfile = os.path.join(outdir, f"lx_plot_{counter:04d}.png")
    plt.tight_layout()
    plt.savefig(outfile)
    print(f"Saving {outfile}")
    
    counter += 1 
    
    plt.close('all')
