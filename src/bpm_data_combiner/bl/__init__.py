"""Business logic for combining data from different devices

This currently is implemented only for BPM readings. Could be
generalised to any readings the carry a unique time stamp
identifier.

* Dispatcher: combine individual record data to one single object.

* Collector: collect data records and combine them together
  assuming that the time stamp identifier is the same for all data
  readings issued at the same time

* Accumulator: accumulate readings together based on the individual
  time count

*Code reuse*: at current stage only the dispatcher depends on
:class:`BPMReading
"""
__all__ = ["accumulator", "collector", "dispatcher", "preprocessor", "event", "monitor_devices", "statistics"]
