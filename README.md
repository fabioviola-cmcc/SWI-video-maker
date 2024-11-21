# SWI Video Maker

This repository hosts a tool intendend to produce a video plotting the Lx and Salinity for a year on a given branch.
It is mostly a set of python script orchestrated by a bash script named `makevideo.sh`.

## Running the tool

An example invocation is:

```
./makevideo.sh "Po Goro" salinity_Po_GORO_2018.nc samples/Po_GORO_LX_2018.csv GORO 0 template_horiz.png 6
```

where the parameters are the following:

- name of the branch (that will be shown on the plots)
- input netcdf file containing the salinity value for all the days in a year
- input csv file containing the Lx value
- output directory where images and videos will be generated
- orientation (0 = horizontal, 1 = vertical)
- template (an image containing a logo to be overlapped)
- fps (the number of frame per seconds. The higher, the faster)

## Setting up the environment

To setup the environment:

```
$ conda create -n lxvid
$ conda activate lxvid
$ conda install python pip
$ pip install xarray netcdf scipy opencv-python Pillow matplotlib cartopy scipy netcdf4
```