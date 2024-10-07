import logging
import sys

# logging.basicConfig(level=logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("bpm-data-combiner")
logger.addHandler(handler)