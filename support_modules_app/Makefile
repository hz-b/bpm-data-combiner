TOP=..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

## Linux

MODULES_Linux = $(foreach dir,$(SHRLIB_SEARCH_DIRS),$(wildcard $(dir)/lib*.so*))
BIN_INSTALLS_Linux = $(MODULES_Linux)
$(info search path: $(SHRLIB_SEARCH_DIRS))
$(info Linux modules: $(MODULES_Linux))

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

