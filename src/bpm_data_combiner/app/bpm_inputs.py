from aioca import camonitor
from bpm_data_combiner.interfaces.controller import ControllerInterface, ValidCommands
from count_down import CountDown
import logging

logger = logging.getLogger("bpm-data-combiner")


class BPMInput:
    def __init__(self, bpm_name: str, controller: ControllerInterface, heart_beat_steps=20):
        self.controller = controller
        self.bpm_name = bpm_name
        # self.input_data = camonitor(f"{bpm_name}:posv", callback=self.on_data)
        # self.sync_stat = camonitor(f"{bpm_name}:clocks:sync_st_m", callback=self.on_sync_stat)
        self.status = CountDown(max_steps=heart_beat_steps)
        #logger.warning(f"{bpm_name}: {self.input_data}, {self.sync_stat}")

    async def on_data(self, values):
        logger.warning(f"new data for {self.bpm_name}")
        self.status.reset()
        self.controller._update(cmd=ValidCommands.reading, dev_name=self.bpm_name, value=values)


    def on_sync_stat(self, value):
        self.controller._update(cmd=ValidCommands.sync_stat, dev_name=self.bpm_name, value=value)
