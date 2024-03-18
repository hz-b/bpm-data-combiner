#!../../bin/linux-x86_64/bpm_data_combiner

#- You may have to change bpm_data_combiner to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"
epicsEnvSet("ENGINEER", "Pierre Schnizer")
epicsEnvSet("LOCATION","Helmholtz Zentrum Berlin / BESSY II")

epicsEnvSet("PREFIX","OrbCol")
epicsEnvSet("REMOTE","Pierre:SIM:")
epicsEnvSet("PYTHONPATH","$(TOP)/src")
# epicsEnvSet("IOC_NAME","${IOC_NAME}")

## Register all support components
dbLoadDatabase "dbd/bpm_data_combiner.dbd"
bpm_data_combiner_registerRecordDeviceDriver pdbbase

## stats records
## dbLoadRecords("db/iocAdminSoft.db", "IOC=$(IOC_NAME)")
## dbLoadRecords("db/iocRelease.db", "IOC=$(IOC_NAME)")

## Load record instances
dbLoadTemplate("db/bpm_dev_input.substitutions", "PREFIX=$(PREFIX)")
# dbLoadRecords("db/bpm_dev_input_offbeat.db", "PREFIX=$(PREFIX)")
dbLoadTemplate("db/bpm.substitutions", "PREFIX=$(PREFIX)")
dbLoadRecords("db/bpm_monitor_overview.db", "PREFIX=$(PREFIX),VIEW=mon")
dbLoadRecords("db/view.db", "PREFIX=$(PREFIX)")
dbLoadRecords("db/bpm_periodic.db", "PREFIX=$(PREFIX)")
dbLoadRecords("db/bpm_bdata.db", "PREFIX=$(PREFIX)")

pydev("from bpm_data_combiner.app.main import update")

#- Set this to see messages from mySub
#-var mySubDebug 1

#- Run this to trace the stages of iocInit
#-traceIocInit

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncExample, "user=mfp"
