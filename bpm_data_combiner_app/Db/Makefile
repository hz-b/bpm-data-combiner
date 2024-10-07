TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# input "mirror" of different bpm's
# pushes data to python world
# DB += bpm_dev_input.db
# bpm_dev_input_TEMPLATE=bpm_dev_input.template
DB += bpm_dev_input_rec.db
DB += bpm_dev_input.substitutions
# views / outputs, gets data from python world
DB += bpm_book_keeping_rec.db
DB += bpm_with_stats_rec.db
DB += bpm_rec.db
DB += bpm.substitutions
DB += bpm_periodic.db
DB += bpm_bdata.db
DB += bpm_monitor_overview.db
# version of the bpm
DB += bpm_data_combinerVersion.db
DB += view.db
DB += bpm_cfg.db

# follow description https://www.slac.stanford.edu/grp/ssrl/spear/epics/site/devIocStats/README_iocAdmin
# IOCstats / admin
# (soft    IOCs)
# HOME_DEVEL=/home/mfp/Devel/github
# IOCADMIN=$(HOME_DEVEL)/iocStats/iocAdmin/

## DB_INSTALLS += $(IOCADMIN)/db/iocAdminSoft.db
## ## # (if required by next step)
## DB_INSTALLS += $(IOCADMIN)/db/access.db
## ## # (optional - ONLY if SCAN monitoring is required)
## DB_INSTALLS += $(IOCADMIN)/db/iocAdminScanMon.db
## ## # If <anyname>.db template is not named <anyname>*.template add
## ## # <anyname>_TEMPLATE = <templatename>

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE

MSI=msi
MSI_FLAGS=-V

bpm_dev_input.db : bpm_dev_input.rec bpm_dev_input.template
	$(MSI) $(MSI_FLAGS) -I$(CURDIR) -o $@ bpm_dev_input.template
