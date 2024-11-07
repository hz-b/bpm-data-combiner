from aioca import caget, caput, camonitor, run

async def do_stuff():
    pv = "BPMZ6D8R:posv"
    # Print out the value reported by PV2.
    print(await caget(pv))

    # Monitor PV3, printing out each update as it is received.
    def callback(value):
        print('callback', value)

    camonitor(pv, callback)

# Now run the camonitor process until interrupted by Ctrl-C.
run(do_stuff(), forever=True)