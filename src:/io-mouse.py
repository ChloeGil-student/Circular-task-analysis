"""Reading MouseReMoCo files (header, samples, markers, records). Only numpy + os."""
import numpy as np


def read_header(path):
    """Line 1 of both files: 'key value;key value;...'. Numbers -> float, the rest stays text."""
    with open(path, encoding="utf-8") as f:
        line = f.readline().strip()
    header = {}
    for item in line.split(";"):
        key, _, value = item.partition(" ")
        try:
            header[key] = float(value)
        except ValueError:
            header[key] = value
    return header

def read_data(path, header=None):
    """Return dict with t (s, from first sample), t_ms, x, y (centered on the task center, y up), inside (bool).
    Raw columns: timestamp, mouseX, mouseY, mouseInTarget (screen pixels, y down)."""
    if header is None:
        header = read_header(path)
    raw = np.genfromtxt(path, delimiter=",", skip_header=4)  # lines 1-3 = header/date/blank, line 4 = column names
    raw = raw[raw[:, 0] > 0]  # the file ends with a junk line "0,0,0,0"
    t_ms = raw[:, 0].astype(np.int64)
    return {
        "t_ms": t_ms,
        "x": raw[:, 1] - header["centerX"],
        "y": header["centerY"] - raw[:, 2],   # flip y so that up is positive, like the expected figures
        "inside": raw[:, 3].astype(bool),
    }


def read_markers(path):
    """Return (markers, ref_table_lines). markers = list of (timestamp_ms, text)."""
    markers, table = [], []
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    in_table = False
    for line in lines[2:]:
        if line.strip().startswith("Var"):
            in_table = True
        if in_table:
            if line.strip():
                table.append(line)
            continue
        parts = line.split(",", 2)
        if len(parts) == 3 and parts[1].isdigit():
            markers.append((int(parts[1]), parts[2]))
    return markers, table

