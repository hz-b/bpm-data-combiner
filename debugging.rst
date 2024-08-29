Debugging the orbit collector or bpm data combiner IOC
------------------------------------------------------

It is assumed that this IOC uses the prefix `OrbCol`.

Checking basic functionalities : information on BPM's
-----------------------------------------------------

Which BPM's are the ones that the collector knowns?

Check the following variable

* `OrbCol:mon:names`: list all the bpms the
   collector knows of

* `OrbCol:mon:active`: which of the BPM's
   are marked as active (i.e. have sent data
   recently)

* `OrbCol:mon:synchronised`: which of the BPM's
   are marked as synchronised on their IOC. Please
   be aware that the BPM's could not be synchronised
   even if the flag it.

* `OrbCol:mon:useable`: which of the BPM's
   does the collector consider as useable


Checking basic functionalities : triggering
-------------------------------------------

* `OrbCol:mon:periodic:cnt': how often has the external
   trigger for producing data been received

   Currently all 2 seconds a new data update is requested
   by some IOC (external to this one) this IOC listens
   to this IOC and sends then an update command to
   python, which in turn will produce new data update

   This count here allows seeing if new data have arrived
   on the EPICS side.




Organisation of variables
-------------------------

* `OrbCol:inp` input variables, thus data expected to be
   read by channel access from some other place

* `OrbCol:mon` monitor variables. These shall tell you
  something of the state of the IOC

* `OrbCol:im` intermediate or internal variables.
   Please be careful if setting them. Please be prepared
   that these names could changes
