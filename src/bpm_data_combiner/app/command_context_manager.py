import io
import traceback
from ..bl.command_round_buffer import CommandRoundBuffer, round_buffer_to_string, dict_to_string
from ..bl.logger import logger
from .view import ViewStringBuffer


class UpdateContext:
    def __init__(self, *, method, rbuffer: CommandRoundBuffer, view: ViewStringBuffer, echo_command=False, only_buffer=True):
        self.method = method
        self.roundbuffer = rbuffer
        self.view = view
        self.only_buffer = only_buffer
        self.echo_command = echo_command

    def __enter__(self):
        if not self.echo_command:
            return

        last = self.roundbuffer.last()
        cmd = " %8s: cmd %4s, kw%s" %( last.dev_name,  last.cmd, dict_to_string(last.kwargs))
        logger.warning("Processing %s", cmd)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return

        self.view.update(
            [f"ERR: {exc_type}", f"ERR {exc_val})"] + round_buffer_to_string(self.roundbuffer)
        )
        if self.only_buffer:
             return

        last = self.roundbuffer.last()

        txt = f" {last.cmd:6s} {dict_to_string(last.kwargs)}: {exc_type}({exc_val})"
        # logger.error(self.roundbuffer)

        logger.error("Could not process command:" + txt)

        logger.error(
            f"Could not process command {last.cmd=}:"
            f"{self.method=} {last.dev_name=} {last.kwargs=}: {exc_type}({exc_val})"
        )

        marker = "-" * 78
        tb_buf = io.StringIO()
        traceback.print_tb(exc_tb, file=tb_buf)
        tb_buf.seek(0)
        logger.error("%s\nTraceback:\n%s\n%s\n", marker, tb_buf.read(), marker)


__all__ = ["UpdateContext"]
