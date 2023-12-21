#!../../bin/linux-x86_64/bpm_dev_sim

#- You may have to change bpm_dev_sim to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

epicsEnvSet("PREFIX","Pierre:SIM:")

## Register all support components
dbLoadDatabase "dbd/bpm_dev_sim.dbd"
bpm_dev_sim_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadTemplate "db/bpm_dev_sim.db", "PREFIX=$(PREFIX)"

#- Set this to see messages from mySub
#-var mySubDebug 1

#- Run this to trace the stages of iocInit
#-traceIocInit

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncExample, "user=mfp"
