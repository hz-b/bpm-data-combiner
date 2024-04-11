TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Install databases, templates & substitutions like this
DB += bpm_dev_sim.db
DB += bpm_dev_sim.rec

# If <anyname>.db template is not named <anyname>*.template add
# <anyname>_TEMPLATE = <templatename>
bpm_dev_sim_TEMPLATE = bpm_dev_sim.template

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE

MSI=msi
MSI_FLAGS=-V

$(COMMON_DIR)/%.db : ../%.template
	$(MSI) $(MSI_FLAGS) -I$(CURDIR) -o $@ $<

