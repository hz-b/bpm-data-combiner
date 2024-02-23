#!/bin/sh

IOC_NAME=`hostname`
T_DIR=`dirname $0`
echo "$IOC_NAME starting bpm data combiner at $T_DIR"

# only one thread to start
export PYDEV_NUM_TREADS=1
${T_DIR}/st.cmd
