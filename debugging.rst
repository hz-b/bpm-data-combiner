Debugging the orbit collector or bpm data combiner IOC
------------------------------------------------------

It is assumed that this IOC uses the prefix `OrbCol`.

Checking basic functionalities : information on BPM's
-----------------------------------------------------

Which BPM's are the ones that the collector knowns?

Check the following variable

* ``OrbCol:mon:names``
   list all the bpms the collector knows of

* ``OrbCol:mon:active``
   which of the BPM's are marked as active (i.e. have sent data
   recently)

* ``OrbCol:mon:synchronised``
   which of the BPM's
   are marked as synchronised on their IOC. Please
   be aware that the BPM's could not be synchronised
   even if the flag it.

* ``OrbCol:mon:usable``
   which of the BPM's
   does the collector consider as useable


Checking basic functionalities : triggering
-------------------------------------------

* ``OrbCol:mon:periodic:cnt``
   how often has the external
   trigger for producing data been received

   Currently all 2 seconds a new data update is requested
   by some IOC (external to this one) this IOC listens
   to this IOC and sends then an update command to
   python, which in turn will produce new data update

   This count here allows seeing if the trigger for
   new (accumulated) data is arriving

   This number should be continously increasing
   with the same rate as the (other) classic bpms are
   updated

Checking basic functionalities : data arriving
----------------------------------------------

* ``OrbCol:mon:col:cnt``
   shows the last count in
   any bpm package arrived from anywhere.

   This count should change very frequently


Check that senders are synchronised
-----------------------------------

**Please note**: these data are only an indication and
not necessarily sufficient.

1. First activate this computation by setting
   ``OrbCol:cfg:comp:median`` to 1
   This will double the computational requirement of this
   IOC and should be deactivated afterwards

2. Check that the IOC has reacted to this request by checking
   ``OrbCol:mon:cfg:comp:median`` has been set to 1

3. Now have a look to
   ``OrbCol:mon:sync:median``
   this value should change frequently. If it does
   not changes at all most probably the bpms are
   not synchronised

   How is this value computed: internally the last cnt
   that has arrived for each channel is tracked. Then the
   median value of this cnt is calculated

   At last look to
   ``OrbCol:mon:sync:offset``. These
   offsets should chance similiarily. Good reference
   values have to be derived from measurments with the
   real BPMs.

   Still these values should not be very large.

   If the offset of the median changes peroidically within the
   same values one can assume that the BPM electronics are
   synchronised


Organisation of variables
-------------------------

* ``OrbCol:inp``
   input variables, thus data expected to be
   read by channel access from some other place

* ``OrbCol:out``
   output variables, thus data provided by
   this IOC.

* ``OrbCol:mon``
   monitor variables. These shall tell you
   something of the state of the IOC

* ``OrbCol:im``
    intermediate or internal variables.
    Please be careful if setting or using them. Please be prepared
    that these names could changes
