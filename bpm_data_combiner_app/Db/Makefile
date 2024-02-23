TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# input "mirror" of different bpm's
# pushes data to python world
DB += bpm_dev_input.db
DB += bpm_dev_input.rec
# views / outputs, gets data from python world
DB += bpm_book_keeping.rec
DB += bpm_with_stats.rec
DB += bpm.rec
DB += bpm.db
DB += bpm_monitor_overview.db
# version of the bpm
DB += bpm_data_combinerVersion.db
DB += view.db

# follow description https://www.slac.stanford.edu/grp/ssrl/spear/epics/site/devIocStats/README_iocAdmin
# IOCstats / admin
# (soft    IOCs)
# HOME_DEVEL=/home/mfp/Devel/github
# IOCADMIN=$(HOME_DEVEL)/iocStats/iocAdmin/

DB_INSTALLS += $(IOCADMIN)/db/iocAdminSoft.db
# (if required by next step)
DB_INSTALLS += $(IOCADMIN)/db/access.db
# (optional - ONLY if SCAN monitoring is required)
DB_INSTALLS += $(IOCADMIN)/db/iocAdminScanMon.db
# If <anyname>.db template is not named <anyname>*.template add
# <anyname>_TEMPLATE = <templatename>

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
