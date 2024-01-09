Combining beam position monitor data in a consistent set
========================================================

Beam position data is published by different input output
controllers. These need to be combined into a consistent
data structure.

For details see

* Product requirements document or `Lastenheft`_
* Scope statement of `Pflichtenheft`_

.. _`Lastenheft` : bpm_data_combiner_app/doc/lastenheft.rst
.. _`Pflichtenheft` : bpm_data_combiner_app/doc/pflichtenheft.rst


For the python part see
 https://hz-b.github.io/bpm-data-combiner/ .



External dependencies
---------------------

* EPICS 7
* PyDevice
