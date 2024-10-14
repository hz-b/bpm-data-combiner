TOP=..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

# find all python modules in bpm_data_combiner and subdirectories, thereof
modules := $(wildcard ../bpm_data_combiner/*.py) $(wildcard ../bpm_data_combiner/*/*.py)
modules += ../bpm_data_combiner/app/mls_sparks
# strip out the .. from path so that they have proper path in lib
PYTHON_IOCMODULE += $(modules:../%=%)

# CFG += CONFIG_MODULE_LIST

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

#CONFIG_MODULE_LIST:
#        echo "BESSY_IOCMODULES_FILE_LIST = $(modules:../%=%)" > $@