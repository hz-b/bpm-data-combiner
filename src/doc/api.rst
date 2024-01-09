API of bpm-data-combiner
========================


The bpm data combiner is designed to work within a PyDevice IOC.
Its interface however is slim, thus it would be possible to
use it by external code too.



TODO's
======

* Implement the controller
* have collector use actual ready devices when
  new reading collection is dispatched


Data models
===========


Status of a BPM
---------------

.. automodule:: bpm_data_combiner.data_model.monitored_device
   :members:
   :undoc-members:
   :show-inheritance:


Data provided by a single IOC
-----------------------------

.. autoclass:: bpm_data_combiner.data_model.bpm_data_reading.BPMReading
   :members:
   :undoc-members:
   :show-inheritance:

Representing the data collected from a set of BPM IOC's
-------------------------------------------------------

.. automodule:: bpm_data_combiner.data_model.bpm_data_collection
   :members:
   :undoc-members:
   :show-inheritance:



Business Logic
==============

.. automodule:: bpm_data_combiner.bl
   :members:
   :undoc-members:
   :show-inheritance:


Monitor devices
---------------

.. automodule:: bpm_data_combiner.bl.monitor_devices
   :members:
   :undoc-members:
   :show-inheritance:


Event
-----

.. automodule:: bpm_data_combiner.bl.event
   :members:
   :undoc-members:
   :show-inheritance:



Dispatcher
----------

.. automodule:: bpm_data_combiner.bl.dispatcher
   :members:
   :undoc-members:
   :show-inheritance:


Collector
---------

.. automodule:: bpm_data_combiner.bl.collector
   :members:
   :undoc-members:
   :show-inheritance:



Accumulator
-----------

.. automodule:: bpm_data_combiner.bl.accumulator
   :members:
   :undoc-members:
   :show-inheritance:
