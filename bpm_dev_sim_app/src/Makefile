TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Use typed rset structure (see 3.16.1 release notes)
USR_CPPFLAGS += -DUSE_TYPED_RSET


# Build an IOC support library
LIBRARY_IOC += bpm_dev_simSupport

# Link locally-provided code into the support library,
# rather than directly into the IOC application, that
# causes problems on Windows DLL builds
bpm_dev_simSupport_SRCS += devbpm_dev_simVersion.c

bpm_dev_simSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

# Auto-generate a header file containing a version string.
# Version comes from the VCS if available, else date+time.
GENVERSION = bpm_dev_simVersion.h
# Macro name
GENVERSIONMACRO = bpm_dev_simVERSION

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

# Link in the code from our support library
bpm_dev_sim_LIBS += bpm_dev_simSupport


# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    bpm_dev_sim_LIBS += qsrv
    bpm_dev_sim_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    bpm_dev_sim_DBD += PVAServerRegister.dbd
    bpm_dev_sim_DBD += qsrv.dbd
endif

# Finally link IOC to the EPICS Base libraries
bpm_dev_sim_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE

# Explicit dependency needed for generated header file
devbpm_dev_simVersion$(DEP): $(COMMON_DIR)/$(GENVERSION)
