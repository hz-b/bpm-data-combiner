import sys
import os.path

t_dir = os.path.dirname(__file__)
if t_dir not in sys.path: sys.path.insert(0, t_dir)

# so it can be used by the pydev
from bpm_data_combiner.app.main import update

def update_print(*, dev_name, **kwargs):
    """a simple first stub to push the data further
    """
    print(f"device {dev_name}: {kwargs}")
