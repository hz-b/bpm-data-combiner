BPM data combiner: requirement specification
============================================

Anstelle eines Pflichtenhefts

Motivation
----------

The beam position monitors of BESSY~II are read out by
electronic units. The existing ones are to be replaced
by new  units.

Below in the text he new units will be called
"instrumentation devices"  (or libera spark?) units.


The data these instrumentation device units provide are
to be comined in such a fashion to

* make it possible to swap out the old units to the new units
  sector per sector

  In the following text the new units are called


* be able to operate the standard slow orbit feedback of the
  BESSY II machine

* provide a consistent data set
  of the beam position monitors

  It shall represent the beam positiion monitor data in a consistent
  fashion to the user as soon as all bpm readers are
  "instrumentation devices units".



Background
----------


Standard operation of the units
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each beam position monitor (BPM) is handled by a dedicated unit.
This unit provides the following data

* x position in nm (or close to that)
* y position in nm (or close to that)
* counts since a synchronisation event: this ensures that all
  units provide a consistent count

This data are provided with an update rate of 0.1 Hz.


Failure modes to consider
~~~~~~~~~~~~~~~~~~~~~~~~~

* Units can be unresponsive: i.e. they can fail to deliver data

* Units can deliver erronous data: the machine operator must be
  able to mark them as erronous (done on the unit or here ? ).



Target:
-------

* Combine beam position monitor data of all beam position monitors in
  a consistent fashion: i.e. the readings of all beam position monitors
  of the new system are provided in a structure.
* Provide the beam position in a manner so that the electronic units can be
  swapped out sector per sector.


Misc: naming
------------

* BPM data combiner: it combines the data to a single set
* BPM data collector: it collects the data of the different units
