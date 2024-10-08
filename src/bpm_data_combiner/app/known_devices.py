#: Todo where to get the device names from
#: use a pycalc record to push it in
from pathlib import Path
from itertools import count

mls_names_file  = Path(__file__).parent / "mls_sparks"

# a perhaps too simple parser
# if you wwant's omething proper consider using
# json
# toml
# happy
# or a real database
with open(mls_names_file, "rt") as fp:
    dev_names_mls = [row.strip() for row in fp.readlines() if row[0] != '#' and row.strip()]

# insert the spare ones ...
def add_spare(dev_names_mls):
    n_per_segment = 7
    segment_enumerate = count()
    for cnt, name in enumerate(dev_names_mls):
        if cnt > 0 and cnt % n_per_segment == 0 :
            yield f"Spare_{next(segment_enumerate):1d}"
        else:
            yield name

dev_names_mls = list(add_spare(dev_names_mls))

dev_names_bessyii = [
    "BPMZ5D8R",
    "BPMZ6D8R",
    "BPMZ7D8R",
    "BPMZ1T8R",
    "BPMZ2T8R",
    "BPMZ3T8R",
    "BPMZ4T8R",
]

dev_names = dev_names_mls

# The BESSY II ring ... with the special ones missing
# should get the standard names
dev_names_for_test = [
    "BPMZ5D1R",
    "BPMZ6D1R",
    "BPMZ7D1R",
    "BPMZ1T1R",
    "BPMZ2T1R",
    "BPMZ3T1R",
    "BPMZ4T1R",
    "BPMZ5T1R",
    "BPMZ6T1R",
    "BPMZ7T1R",
    "BPMZ1D2R",
    "BPMZ2D2R",
    "BPMZ3D2R",
    "BPMZ4D2R",
    "BPMZ5D2R",
    "BPMZ6D2R",
    "BPMZ7D2R",
    "BPMZ1T2R",
    "BPMZ2T2R",
    "BPMZ3T2R",
    "BPMZ4T2R",
    "BPMZ5T2R",
    "BPMZ6T2R",
    "BPMZ7T2R",
    "BPMZ1D3R",
    "BPMZ2D3R",
    "BPMZ3D3R",
    "BPMZ4D3R",
    "BPMZ5D3R",
    "BPMZ6D3R",
    "BPMZ7D3R",
    "BPMZ1T3R",
    "BPMZ2T3R",
    "BPMZ3T3R",
    "BPMZ4T3R",
    "BPMZ5T3R",
    "BPMZ6T3R",
    "BPMZ7T3R",
    "BPMZ1D4R",
    "BPMZ2D4R",
    "BPMZ3D4R",
    "BPMZ4D4R",
    "BPMZ5D4R",
    "BPMZ6D4R",
    "BPMZ7D4R",
    "BPMZ1T4R",
    "BPMZ2T4R",
    "BPMZ3T4R",
    "BPMZ4T4R",
    "BPMZ5T4R",
    "BPMZ6T4R",
    "BPMZ7T4R",
    "BPMZ1D5R",
    "BPMZ2D5R",
    "BPMZ3D5R",
    "BPMZ4D5R",
    "BPMZ5D5R",
    "BPMZ6D5R",
    "BPMZ7D5R",
    "BPMZ1T5R",
    "BPMZ2T5R",
    "BPMZ3T5R",
    "BPMZ4T5R",
    "BPMZ5T5R",
    "BPMZ6T5R",
    "BPMZ7T5R",
    "BPMZ1D6R",
    "BPMZ2D6R",
    "BPMZ3D6R",
    "BPMZ4D6R",
    "BPMZ5D6R",
    "BPMZ6D6R",
    "BPMZ7D6R",
    "BPMZ1T6R",
    "BPMZ2T6R",
    "BPMZ3T6R",
    "BPMZ4T6R",
    "BPMZ5T6R",
    "BPMZ6T6R",
    "BPMZ7T6R",
    "BPMZ1D7R",
    "BPMZ2D7R",
    "BPMZ3D7R",
    "BPMZ4D7R",
    "BPMZ5D7R",
    "BPMZ6D7R",
    "BPMZ7D7R",
    "BPMZ1T7R",
    "BPMZ2T7R",
    "BPMZ3T7R",
    "BPMZ4T7R",
    "BPMZ5T7R",
    "BPMZ6T7R",
    "BPMZ7T7R",
    "BPMZ1D8R",
    "BPMZ2D8R",
    "BPMZ3D8R",
    "BPMZ4D8R",
]

# repetition whats already available
# adding a d for twin
dev_names_for_test += [
    "BPMZ5D8RD",
    "BPMZ6D8RD",
    "BPMZ7D8RD",
    "BPMZ1T8RD",
    "BPMZ2T8RD",
    "BPMZ3T8RD",
    "BPMZ4T8RD",
    "BPMZ5T8RD",
    "BPMZ6T8RD",
    "BPMZ7T8RD",
    "BPMZ1D1RD",
    "BPMZ2D1RD",
    "BPMZ3D1RD",
    "BPMZ4D1RD",
    "BPMZ5D1RD",
    "BPMZ6D1RD",
    "BPMZ7D1RD",
    "BPMZ1T1RD",
    "BPMZ2T1RD",
    "BPMZ3T1RD",
    "BPMZ4T1RD",
    "BPMZ5T1RD",
    "BPMZ6T1RD",
    "BPMZ7T1RD",
    "BPMZ1D2RD",
    "BPMZ2D2RD",
    "BPMZ3D2RD",
    "BPMZ4D2RD",
    "BPMZ5D2RD",
    "BPMZ6D2RD",
    "BPMZ7D2RD",
    "BPMZ1T2RD",
    "BPMZ2T2RD",
    "BPMZ3T2RD",
    "BPMZ4T2RD",
    "BPMZ5T2RD",
    "BPMZ6T2RD",
    "BPMZ7T2RD",
    "BPMZ1D3RD",
    "BPMZ2D3RD",
    "BPMZ3D3RD",
    "BPMZ4D3RD",
    "BPMZ5D3RD",
    "BPMZ6D3RD",
    "BPMZ7D3RD",
    "BPMZ1T3RD",
    "BPMZ2T3RD",
    "BPMZ3T3RD",
    "BPMZ4T3RD",
    "BPMZ5T3RD",
    "BPMZ6T3RD",
    "BPMZ7T3RD",
    "BPMZ1D4RD",
    "BPMZ2D4RD",
    "BPMZ3D4RD",
    "BPMZ4D4RD",
    "BPMZ5D4RD",
    "BPMZ6D4RD",
    "BPMZ7D4RD",
    "BPMZ1T4RD",
    "BPMZ2T4RD",
    "BPMZ3T4RD",
    "BPMZ4T4RD",
    "BPMZ5T4RD",
    "BPMZ6T4RD",
    "BPMZ7T4RD",
    "BPMZ1D5RD",
    "BPMZ2D5RD",
    "BPMZ3D5RD",
    "BPMZ4D5RD",
    "BPMZ5D5RD",
    "BPMZ6D5RD",
    "BPMZ7D5RD",
    "BPMZ1T5RD",
    "BPMZ2T5RD",
    "BPMZ3T5RD",
    "BPMZ4T5RD",
    "BPMZ5T5RD",
    "BPMZ6T5RD",
    "BPMZ7T5RD",
    "BPMZ1D6RD",
    "BPMZ2D6RD",
    "BPMZ3D6RD",
    "BPMZ4D6RD",
    "BPMZ5D6RD",
    "BPMZ6D6RD",
    "BPMZ7D6RD",
    "BPMZ1T6RD",
    "BPMZ2T6RD",
    "BPMZ3T6RD",
    "BPMZ4T6RD",
    "BPMZ5T6RD",
    "BPMZ6T6RD",
    "BPMZ7T6RD",
    "BPMZ1D7RD",
    "BPMZ2D7RD",
    "BPMZ3D7RD",
    "BPMZ4D7RD",
    "BPMZ5D7RD",
    "BPMZ6D7RD",
    "BPMZ7D7RD",
    "BPMZ1T7RD",
    "BPMZ2T7RD",
    "BPMZ3T7RD",
    "BPMZ4T7RD",
    "BPMZ5T7RD",
    "BPMZ6T7RD",
    "BPMZ7T7RD",
    "BPMZ1D8RD",
    "BPMZ2D8RD",
    "BPMZ3D8RD",
    "BPMZ4D8RD",
    "BPMZ5D8RD",
    "BPMZ6D8RD",
    "BPMZ7D8RD",
    "BPMZ1T8RD",
    "BPMZ2T8RD",
    "BPMZ3T8RD",
    "BPMZ4T8RD",
    "BPMZ5T8RD",
    "BPMZ6T8RD",
    "BPMZ7T8RD",
    "BPMZ1D1RD",
    "BPMZ2D1RD",
    "BPMZ3D1RD",
    "BPMZ4D1RD",
]
