Combining beam position monitor data in a consistent set
========================================================

Beam position data is published by different input output
controllers. These need to be combined into a consistent
data structure.

For details see:

* Product requirements document or `Lastenheft`_
* Scope statement of `Pflichtenheft`_

.. _`Lastenheft` : src/doc/requirements/lastenheft.rst
.. _`Pflichtenheft` : src/doc/requirements/pflichtenheft.rst

The functionallity is implemented as  EPICS IOC's. A significant
fraction is implemented in python using pydevice. All python code
is implemented in the python module `bpm-data-combiner`. Have a
look to  https://hz-b.github.io/bpm-data-combiner/ for its
documentation.

Debugging IOC
-------------

see description in debugging functionality in `debugging`_

.. _`debugging` : src/doc/debugging.rst

External dependencies
---------------------

* EPICS 7
* PyDevice
* numpy
