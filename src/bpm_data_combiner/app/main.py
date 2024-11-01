"""

Todo:
   add a reset command
"""
from datetime import datetime
import sys

from ..bl.command_round_buffer import CommandRoundBuffer
from ..data_model.command import Command
from .command_context_manager import UpdateContext
from .facade import Facade, logger

stream = sys.stdout

facade = Facade()
rbuffer = CommandRoundBuffer(maxsize=50)


def update(*, dev_name, tpro=False, **kwargs):
    """Inform the dispatcher associated to the device that new data is available"""

    cmd = next(iter(kwargs))
    try:
        dc = Command(
            cmd=cmd, dev_name=dev_name, kwargs=kwargs, timestamp=datetime.now()
        )
        rbuffer.append(dc)
    except:
        logger.error("Failed to prepare wrapper info")
        raise
    r = None
    with UpdateContext(
        method=None,
        rbuffer=rbuffer,
        view=facade.views.monitor_update_cmd_errors,
        only_buffer=not bool(tpro),
    ):
        r = facade.update(cmd=cmd, dev_name=dev_name, tpro=tpro, **kwargs)

    # todo: does pydevice expects a return on the function ?
    if r is None:
        r = kwargs.get("val", -1)
    return r


__all__ = ["update"]
