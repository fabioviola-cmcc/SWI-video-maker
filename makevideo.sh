#!/bin/bash

################################################
#
# Input params
#
################################################

BRANCH_NAME=$1
INPUT_NC_FILE=$2
INPUT_CSV_FILE=$3
OUTPUT_DIR=$4
ORIENTATION=$5
TEMPLATE=$6
FPS=$7

################################################
#
# init
#
################################################

# create output directory if it does not exist
if [[ ! -d  ${OUTPUT_DIR} ]]; then
    mkdir ${OUTPUT_DIR} -v
fi

################################################
#
# produce salinity and lx images
#
################################################

# plot salinity
python plot_salinity.py ${INPUT_NC_FILE} ${INPUT_CSV_FILE} "${BRANCH_NAME}" "$OUTPUT_DIR"

# plot lx
python plot_lx.py "${BRANCH_NAME}" ${INPUT_CSV_FILE} ${OUTPUT_DIR}

# merge images
python merge_images.py "$OUTPUT_DIR" ${ORIENTATION} ${TEMPLATE}


################################################
#
# input params
#
################################################

# make video
python make_video.py ${OUTPUT_DIR} ${ORIENTATION} ${FPS}
