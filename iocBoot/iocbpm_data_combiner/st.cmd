#!../../bin/linux-x86_64/bpm_data_combiner

#- You may have to change bpm_data_combiner to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

epicsEnvSet("PREFIX","Pierre:COM:")
# epicsEnvSet("REMOTE","Pierre:SIM:")
epicsEnvSet("REMOTE","")
epicsEnvSet("PYTHONPATH","$(TOP)/src")

## Register all support components
dbLoadDatabase "dbd/bpm_data_combiner.dbd"
bpm_data_combiner_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadRecords("db/bpm_dev_input_offbeat.db", "PREFIX=$(PREFIX)")
dbLoadRecords("db/bpm_dev_input_cnt.db", "PREFIX=$(PREFIX)")
dbLoadTemplate("db/bpm_dev_input.db", "PREFIX=$(PREFIX)", "REMOTE=$(REMOTE)")
dbLoadTemplate("db/bpm.db", "PREFIX=$(PREFIX)")
dbLoadRecords "db/bpm_data_combinerVersion.db", "user=mfp"

pydev("from bpm_data_combiner.app.main import update")

#- Set this to see messages from mySub
#-var mySubDebug 1

#- Run this to trace the stages of iocInit
#-traceIocInit

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncExample, "user=mfp"
