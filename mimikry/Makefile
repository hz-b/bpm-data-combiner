EPICS_BASE?=/home/mfp/Devel/github/epics-base/
T_A?=linux-x86_64
MSI=$(EPICS_BASE)/bin/$(T_A)/msi

RM=rm
RMFLAGS=-f
CAT=cat

DB_FILES=classic-bpm-misc.db
DB_BUILD_FILES=classic-bpm-stat.db
TARGET=classic-bpm.db

all : $(TARGET) $(DB_FILES)

$(TARGET) : $(DB_FILES) $(DB_BUILD_FILES)
	cat $^ > $@

clean:
	$(RM) $(RMFLAGS) $(DB_BUILD_FILES)


%.db : %.template
	$(MSI) -o $@ -S $^
