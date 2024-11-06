import asyncio

from aioca import camonitor
from softioc import softioc, builder, asyncio_dispatcher

from collector import UnknownDeviceNameError
from .controller import Controller
from .known_devices import dev_names_mls as _dev_names
from .known_devices import dev_names_bessyii as _dev_names
from ..errors import NoCollectionsError
from ..bl.logger import logger


# each one separately ... waiting eternally for ca monitor to make the connection
async def bpm_data_receive(controller, dev_name):
    def new_reading(value):
        try:
            controller.update(dev_name=dev_name, reading=value)
        except UnknownDeviceNameError as exc:
            logger.warning(f"Could not update data for {dev_name}: {exc}")
        except Exception as exc:
            logger.error(f"processing new data for {dev_name}:{type(exc)}, {exc}")
            raise exc

    data_pv = dev_name + ":posv"
    camonitor(data_pv, new_reading)
    print(f"bpm data from: {dev_name} using {data_pv}")

async def bpm_data_sync_stat(controller, dev_name):
    def sync_stat(value):
        print(f"bpm sync_stat: {dev_name}, {value}")
        try:
            controller.update(dev_name=dev_name, sync_stat=value)
        except UnknownDeviceNameError as exc:
            logger.error(f"Could not update sync_stat for {dev_name}: {exc}")


    sync_stat_pv = dev_name + ":clocks:sync_st_m"
    camonitor(sync_stat_pv, sync_stat)
    print(f"monitoring bpm sync_stat: {dev_name} using {sync_stat_pv}")


async def heart_beat(controller):
    """For processing if devices are active
    needs to be called periodically
    """
    while True:
        controller.heart_beat()
        await asyncio.sleep(.5)


async def periodic_update(controller):
    while True:
        # first data after 2 seconds ...
        await asyncio.sleep(2.0)
        try:
            controller.periodic_trigger()
        except NoCollectionsError as nc:
            logger.error(f"periodic trigger raised NoCollectionsError {nc}")
        except Exception as exc:
            raise


def main():
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.SetDeviceName("OrbCol")
    controller = Controller(prefix="", device_names=_dev_names)
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    # print(f"bpm data: {dev_name}, {value}")
    for dev_name in list(controller.dev_name_index):
        dispatcher(bpm_data_receive, func_args=(controller, dev_name,))
        dispatcher(bpm_data_sync_stat, func_args=(controller, dev_name,))
    dispatcher(heart_beat, func_args=(controller,))
    dispatcher(periodic_update, func_args=(controller,))

    # Finally leave the IOC running with an interactive shell.
    softioc.interactive_ioc(globals())
