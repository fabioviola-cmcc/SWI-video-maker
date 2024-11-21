#!/usr/bin/python3
#
# This script is intended to plot the salinity
# and salt wedge intrusion length
# - salinity NetCDF file
# - the input CSV file for Lx
# - the branch name
# - the output directory

##################################################
#
# requirements
#
##################################################

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import warnings
import numpy
import sys
import csv
import pdb
import os

# Suppress specific warnings by matching the message
warnings.filterwarnings("ignore", 
    message="The .xlabels_top attribute is deprecated. Please use .top_labels to toggle visibility instead.")
warnings.filterwarnings("ignore", 
    message="The .ylabels_right attribute is deprecated. Please use .right_labels to toggle visibility instead.")


##################################################
#
# plot_salinity
#
##################################################

def plot_salinity(nc_file, csv_file, branch_name, outdir):
    
    # Open the NetCDF file with xarray
    ds = xr.open_dataset(nc_file)

    # Open the CSV file and read it into a list
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        csv_data = list(reader)

    # Extract the variables
    lat = ds['lat']
    lon = ds['lon']
    salinity = ds['salinity']
    minsal = numpy.nanmin(salinity)
    maxsal = numpy.nanmax(salinity)

    # Extract bounding box
    max_lat = numpy.max(ds['lat'])
    max_lon = numpy.max(ds['lon'])
    min_lat = numpy.min(ds['lat'])
    min_lon = numpy.min(ds['lon'])

    # Loop through each time step
    counter = 0
    for t in salinity.time:
        plt.figure(dpi=300)

        # Set up the map projection and axes
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines(linewidth=0.1)
                
        # Add gridlines    
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=0.1, color='gray', alpha=0.5, linestyle='--')
    
        # Set font size for x-tick and y-tick labels
        gl.xlabel_style = {'size': 7}
        gl.ylabel_style = {'size': 7}
        gl.xlabels_top = False
        gl.ylabels_right = False

        # Plot salinity
        salinity_at_t = salinity.sel(time=t)
        im = salinity_at_t.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='viridis', add_colorbar=False, vmax=maxsal)

        # Add a colorbar label
        cbar = plt.colorbar(im, label='Salinity (psu)', orientation='vertical', shrink=0.5)
        cbar.set_label('Salinity (psu)', fontsize=7, labelpad=15)
        cbar.ax.tick_params(labelsize=7)  # Set colorbar tick label size
            
        # Read data from the csv
        csv_line = csv_data[counter + 1]
        
        # Add a marker for Lx
        lx_lat = csv_line[1]
        lx_lon = csv_line[2]
        ax.plot(float(lx_lon), float(lx_lat), color='red', marker='x') # , markersize=configDict["pointsSize"])
        
        # determine the date        
        cdate = csv_data[counter + 1][0]
        
        # title and labels
        plt.title(f'{branch_name} salinity on %s' % (cdate), fontsize=10)
        plt.ylabel('Latitude (degN)', fontsize=10, labelpad=10)
        plt.xlabel('Longitude (degE)', fontsize=10)

        # avoid white spaces around
        plt.tight_layout()
        
        # save the figure
        outfile = os.path.join(outdir, f"salinity_plot_{counter:04d}.png")
        print(f"Saving plot {outfile}")
        plt.savefig(outfile, bbox_inches='tight', pad_inches=0.4)

        plt.close()

        counter += 1


##################################################
#
# main
#
##################################################

if __name__ == "__main__":

    # read input params
    salinity_file = sys.argv[1]
    lx_file = sys.argv[2]
    branch_name = sys.argv[3]
    outdir = sys.argv[4]

    # plot the nc file
    plot_salinity(salinity_file, lx_file, branch_name, outdir)
