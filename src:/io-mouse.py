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

