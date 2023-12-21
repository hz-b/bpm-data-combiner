Scope statement
===============

Anstelle eines Lastenhefts

Background
----------
BESSY II will be equipped with new BPMs successively. For a substantial period,
there will be hybrid operation of existing BPMs and new BPMs (Libera Spark).
The intention is to provide data structures similar to the old BPMs generated
from the new data sources to enable operation of applications like slow orbit
feedback during the transition.

The control system to be used is `EPICS`.

Data provided by Libera Spark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Libera Spark units provide, besides many other PVs not relevant for Orbit Feedback:

* x position
* y position
* Time since synchronisation (in steps of internal samples)

All these are currently provided in individual PVs. The synchronisation of data production
across several BPM units will be achieved by a seperate process using the timing system.

To begin with, the data sources from different BPMs should be regarded as asynchronous.


Data provided by the existing units
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* x position
* y position
* status like Power and Automatic Gain

All readings from BPMs in one cell are transmitted in one PV (one waveform), with the
elements representing the individual BPMs. The transmission across cells is performed
by a trigger PV at a pace of 0.5Hz.


Output to be provided by the combiner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provide the beam position in a consistent set in the format of the existing cell IOCs.

PVs of the new units will need to be collected for all units in a cell (7-8) and averaged
over time before output triggered by the existing trigger PV.
