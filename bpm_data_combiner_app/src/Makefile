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
PROD_IOC = bpm_data_combiner

# bpm_data_combiner.dbd will be created and installed
DBD += bpm_data_combiner.dbd

bpm_data_combiner_DBD += base.dbd

# bpm_data_combiner.dbd will include these files:
bpm_data_combiner_DBD += pydev.dbd
bpm_data_combiner_LIBS += pydev

# bpm_data_combiner_registerRecordDeviceDriver.cpp derives from bpm_data_combiner.dbd
bpm_data_combiner_SRCS += bpm_data_combiner_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
bpm_data_combiner_SRCS_DEFAULT += bpm_data_combinerMain.cpp
bpm_data_combiner_SRCS_vxWorks += -nil-

# Link in the code from our support library
bpm_data_combiner_LIBS += bpm_data_combinerSupport

# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    bpm_data_combiner_LIBS += qsrv
    bpm_data_combiner_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    bpm_data_combiner_DBD += PVAServerRegister.dbd
    bpm_data_combiner_DBD += qsrv.dbd
endif

# Finally link IOC to the EPICS Base libraries
bpm_data_combiner_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
