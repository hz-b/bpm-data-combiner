#!/bin/sh

# for operating on 
#currently sciencec1c
HOST_MACHINE=192.168.211.42
EPICS_CA_ADDR_LIST=$HOST_MACHINE

export EPICS_CA_ADDR_LIST

softIoc -m 'INP=Pierre:COM,REFERENCE=MDIZ1D6G,PREFIX=MDIZ1D8G' \
	-d classic-bpm.db
 
