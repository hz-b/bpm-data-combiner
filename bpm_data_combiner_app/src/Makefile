TOP=../..

include $(TOP)/configure/CONFIG
include $(PYDEVICE)/configure/CONFIG.PyDevice
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

CROSS_COMPILER_TARGET_ARCHS=

# Use typed rset structure (see 3.16.1 release notes)
USR_CPPFLAGS += -DUSE_TYPED_RSET

# Auto-generate a header file containing a version string.
# Version comes from the VCS if available, else date+time.
# Build the IOC application
PROD_IOC = bpm_data_combiner

# bpm_data_combiner.dbd will be created and installed
DBD += bpm_data_combiner.dbd

bpm_data_combiner_DBD += base.dbd
bpm_data_combiner_DBD += caPutLog.dbd
bpm_data_combiner_DBD += asSupport.dbd
bpm_data_combiner_DBD += devDistVersion.dbd
bpm_data_combiner_DBD += devIocStats.dbd
#bpm_data_combiner_DBD += iocshGlobalCommands.dbd

bpm_data_combiner_LIBS += caPutLog
bpm_data_combiner_LIBS += autosave
bpm_data_combiner_LIBS += devDistVersion
bpm_data_combiner_LIBS += devIocStats

# bpm_data_combiner.dbd will include these files:
bpm_data_combiner_DBD += pydev.dbd
bpm_data_combiner_DBD += pydev315.dbd
bpm_data_combiner_DBD += pycalcRecord.dbd
bpm_data_combiner_LIBS += pydev

# bpm_data_combiner_registerRecordDeviceDriver.cpp derives from bpm_data_combiner.dbd
bpm_data_combiner_SRCS += bpm_data_combiner_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
bpm_data_combiner_SRCS_DEFAULT += bpm_data_combinerMain.cpp
#bpm_data_combiner_SRCS_vxWorks += -nil-

# Link in the code from our support library
bpm_data_combiner_LIBS +=  $(EPICS_BASE_IOC_LIBS)

# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    bpm_data_combiner_LIBS += qsrv
    bpm_data_combiner_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    bpm_data_combiner_DBD += PVAServerRegister.dbd
    bpm_data_combiner_DBD += qsrv.dbd
endif

# linker definitions for rpath
STATIC_BUILD = NO
LINKER_USE_RPATH = NO

USR_LDFLAGS += '-Wl,--no-as-needed,-rpath,$$ORIGIN'

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
