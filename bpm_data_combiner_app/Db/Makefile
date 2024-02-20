TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# input "mirror" of different bpm's
# pushes data to python world
DB += bpm_dev_input_offbeat.db
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

# If <anyname>.db template is not named <anyname>*.template add
# <anyname>_TEMPLATE = <templatename>

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
