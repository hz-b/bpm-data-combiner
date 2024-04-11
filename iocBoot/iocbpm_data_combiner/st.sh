#!/bin/sh

EPICS_BASE=/opt/Epics/sumo/build/BASE/R3-15-8-bessy4+BII-063/
T_A=linux-x86_64
EPICS_BASE_LIB_PATH="$EPICS_BASE"/lib/"$T_A"

if [ -z  $LD_LIBRARY_PATH ]
then
    LD_LIBRARY_PATH="$EPICS_BASE_LIB_PATH"
else
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH":"$EPICS_BASE_LIB_PATH"
fi
export LD_LIBRARY_PATH

IOC_NAME=`hostname`
T_DIR=`dirname $0`

export IOC_NAME

echo "$IOC_NAME starting bpm data combiner at $T_DIR"

# only one thread to start
export PYDEV_NUM_TREADS=1
${T_DIR}/st.cmd
