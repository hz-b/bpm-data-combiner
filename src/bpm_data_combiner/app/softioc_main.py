import asyncio
import logging

from softioc import softioc, builder, asyncio_dispatcher
from aioca import camonitor, DBR_LONG

from collector import UnknownDeviceNameError
from .controller import Controller
from .known_devices import dev_names_mls as _dev_names
from .known_devices import dev_names_bessyii as _dev_names

logger = logging.getLogger("bpm-data-combiner")

dispatcher = asyncio_dispatcher.AsyncioDispatcher()

builder.SetDeviceName("OrbCol")

controller = Controller(prefix="", device_names=_dev_names)

builder.LoadDatabase()
softioc.iocInit(dispatcher)


# each one separately ... waiting eternally for ca monitor to make the connection
async def bpm_data_receive(dev_name):
    def new_reading(value):
        try:
            controller.update(dev_name=dev_name, reading=value)
        except UnknownDeviceNameError as exc:
            logger.warning(f"Could not update data for {dev_name}: {exc}")
        except Exception as exc:
            logger.error(f"processing new data for {dev_name}:{type(exc)}, {exc}")
            raise exc
        # print(f"bpm data: {dev_name}, {value}")

    data_pv = dev_name + ":posv"
    camonitor(pv=data_pv, callback=new_reading)


async def bpm_data_sync_stat(dev_name):
    def sync_stat(value):
        print(f"bpm sync_stat: {dev_name}, {value}")
        try:
            controller.update(dev_name=dev_name, sync_stat=value)
        except UnknownDeviceNameError as exc:
            logger.error(f"Could not update sync_stat for {dev_name}: {exc}")


    sync_stat_pv = dev_name + ":clocks:sync_st_m"
    camonitor(sync_stat_pv, sync_stat)
    print(f"monitoring bpm sync_stat: {dev_name} using {sync_stat_pv}")


async def heart_beat():
    """For processing if devices are active
    needs to be called periodically
    """
    while True:
        controller.heart_beat()
        await asyncio.sleep(.5)

async def periodic_update():
    while True:
        # first data after 2 seconds ...
        await asyncio.sleep(2.0)
        controller.periodic_trigger()

for dev_name in list(controller.dev_name_index):
    dispatcher(bpm_data_receive, func_args=(dev_name,))
    dispatcher(bpm_data_sync_stat, func_args=(dev_name,))

dispatcher(heart_beat)
dispatcher(periodic_update)

# Finally leave the IOC running with an interactive shell.
softioc.interactive_ioc(globals())
