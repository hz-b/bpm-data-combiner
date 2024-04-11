TOP=../..

include $(TOP)/configure/CONFIG
include $(PYDEVICE)/configure/CONFIG.PyDevice
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Use typed rset structure (see 3.16.1 release notes)
USR_CPPFLAGS += -DUSE_TYPED_RSET

# Auto-generate a header file containing a version string.
# Version comes from the VCS if available, else date+time.
# Build the IOC application
ifeq ($(EPICS_HOST_ARCH),$(T_A))
PROD_IOC = bpm_data_combiner
endif # EPICS_HOST_ARCH

# bpm_data_combinerSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

# bpm_data_combiner.dbd will be created and installed
DBD += bpm_data_combiner.dbd

bpm_data_combiner_DBD += base.dbd
bpm_data_combiner_SRCS += array_forward.cpp
bpm_data_combiner_DBD += array_forward.dbd

# bpm_data_combiner.dbd will include these files:
bpm_data_combiner_DBD += pydev.dbd
bpm_data_combiner_DBD += pydev315.dbd
bpm_data_combiner_LIBS += pydev

# bpm_data_combiner_registerRecordDeviceDriver.cpp derives from bpm_data_combiner.dbd
bpm_data_combiner_SRCS += bpm_data_combiner_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
bpm_data_combiner_SRCS_DEFAULT += bpm_data_combinerMain.cpp
bpm_data_combiner_SRCS_vxWorks += -nil-

# bpm_data_combinerSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

# Link in the code from our support library
bpm_data_combiner_LIBS += $(EPICS_BASE_IOC_LIBS)

# To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file
ifneq ($(SNCSEQ),)
    # Build sncExample into bpm_data_combinerSupport
    sncExample_SNCFLAGS += +r
    bpm_data_combiner_DBD += sncExample.dbd
    # A .stt sequence program is *not* pre-processed:
    bpm_data_combinerSupport_SRCS += sncExample.stt
    bpm_data_combinerSupport_LIBS += seq pv
    bpm_data_combiner_LIBS += seq pv

    # Build sncProgram as a standalone program
    PROD_HOST += sncProgram
    sncProgram_SNCFLAGS += +m
    # A .st sequence program *is* pre-processed:
    sncProgram_SRCS += sncProgram.st
    sncProgram_LIBS += seq pv
    sncProgram_LIBS += $(EPICS_BASE_HOST_LIBS)
endif

# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    bpm_data_combiner_LIBS += qsrv
    bpm_data_combiner_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    bpm_data_combiner_DBD += PVAServerRegister.dbd
    bpm_data_combiner_DBD += qsrv.dbd
endif

WITH_IOCSTATS=1
ifeq ($(WITH_IOCSTATS),1)
  bpm_data_combiner_LIBS += devIocStats
  bpm_data_combiner_DBD += devIocStats.dbd iocAdmin.dbd
endif



# Finally link IOC to the EPICS Base libraries
bpm_data_combiner_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
