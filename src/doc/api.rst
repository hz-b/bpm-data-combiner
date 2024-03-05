API of bpm-data-combiner
========================


The bpm data combiner is designed to work within a PyDevice IOC.
Its interface however is slim, thus it would be possible to
use it by external code too.



TODO's
------

* Implement the controller
* have collector use actual ready devices when
  new reading collection is dispatched



Data model
----------

Status of a BPM
~~~~~~~~~~~~~~~

.. automodule:: bpm_data_combiner.data_model.monitored_device
   :members:
   :show-inheritance:


Data provided by a single IOC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bpm_data_combiner.data_model.bpm_data_reading.BPMReading
   :members:
   :show-inheritance:



Representing the data collected from a set of BPM IOC's
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: bpm_data_combiner.data_model.bpm_data_collection
   :members:
   :show-inheritance:
