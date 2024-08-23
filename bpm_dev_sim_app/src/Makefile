TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Use typed rset structure (see 3.16.1 release notes)
USR_CPPFLAGS += -DUSE_TYPED_RSET


# Build an IOC support library
LIBRARY_IOC += bpm_dev_simSupport

bpm_dev_simSupport_LIBS += $(EPICS_BASE_IOC_LIBS)
bpm_dev_simSupport_SRCS += empty.c

# Build the IOC application
PROD_IOC = bpm_dev_sim

# bpm_dev_sim.dbd will be created and installed
DBD += bpm_dev_sim.dbd

# bpm_dev_sim.dbd will include these files:
bpm_dev_sim_DBD += base.dbd

# bpm_dev_sim_registerRecordDeviceDriver.cpp derives from bpm_dev_sim.dbd
bpm_dev_sim_SRCS += bpm_dev_sim_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
bpm_dev_sim_SRCS_DEFAULT += bpm_dev_simMain.cpp
bpm_dev_sim_SRCS_vxWorks += -nil-

# bpm_dev_simSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

# Link in the code from our support library
bpm_dev_sim_LIBS += bpm_dev_simSupport

bpm_dev_sim_DBD += concatRecord.dbd
bpm_dev_sim_LIBS += concatRecord

# Add all the support libraries needed by this IOC
#


# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    bpm_dev_sim_LIBS += qsrv
    bpm_dev_sim_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    bpm_dev_sim_DBD += PVAServerRegister.dbd
    bpm_dev_sim_DBD += qsrv.dbd
endif

# Finally link IOC to the EPICS Base libraries
bpm_dev_sim_LIBS += bpm_dev_simSupport
bpm_dev_sim_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
