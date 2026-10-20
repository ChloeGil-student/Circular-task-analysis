"""Plotting functions for the circular steering task.
They use the outputs of src/io_mouse.py (header, data, records). Only numpy + matplotlib."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


def record_mask(data, record):
    """Boolean mask of the samples inside one record window (t_start_ms, t_end_ms)."""
    t_start, t_end = record
    return (data["t_ms"] >= t_start) & (data["t_ms"] <= t_end)


def time_s(data):
    """Time in seconds since the first sample of the file."""
    return (data["t_ms"] - data["t_ms"][0]) / 1000


def target_radii(header):
    """Inner and outer radii of the zone where mouseInTarget = 1 (see isInside in the MouseReMoCo doc):
    the cursor center must stay cursorRadius away from both circles, and the external border is drawn inside."""
    r_in = header["internalRadius"] + header["cursorRadius"]
    r_out = header["externalRadius"] - header["cursorRadius"] - header["borderRadius"]
    return r_in, r_out


def plot_raw_time_series(data, records):
    """x and y over time for all records, with vertical lines at record start (black) and end (red)."""
    t = time_s(data)
    t0 = data["t_ms"][0]
    plt.figure(figsize=(9, 3.5))
    for i, rec in enumerate(records):
        m = record_mask(data, rec)
        plt.plot(t[m], data["x"][m], ".", color="tab:blue", label="x position" if i == 0 else None)
        plt.plot(t[m], data["y"][m], ".", color="tab:orange", label="y position" if i == 0 else None)
    for i, (t_start, t_end) in enumerate(records):
        plt.axvline((t_start - t0) / 1000, color="black", linestyle="--", label="record start" if i == 0 else None)
        plt.axvline((t_end - t0) / 1000, color="red", linestyle="--", label="record end" if i == 0 else None)
    plt.title("Raw time series data")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_raw_trajectory(data, records, header):
    """Trajectory of all records (one line per record), inside samples in green, target limits in red."""
    r_in, r_out = target_radii(header)
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, rec in enumerate(records):
        m = record_mask(data, rec)
        ax.plot(data["x"][m], data["y"][m], "-", color="tab:blue", label="trajectory" if i == 0 else None)
        ok = m & data["inside"]
        ax.plot(data["x"][ok], data["y"][ok], "o", color="tab:green", label="inside target" if i == 0 else None)
    ax.add_patch(Circle((0, 0), r_out, fill=False, edgecolor="red", label="target"))
    ax.add_patch(Circle((0, 0), r_in, fill=False, edgecolor="red"))
    ax.set_aspect("equal")
    ax.set_title("Raw trajectory data")
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.legend()
    plt.tight_layout()
    plt.show()


def print_record_summary(data, records):
    """Number of samples, time range, duration and mean sampling rate of each record."""
    t = time_s(data)
    print(f"Number of records: {len(records)}")
    for i, rec in enumerate(records):
        m = record_mask(data, rec)
        tr = t[m]
        n = m.sum()
        duration = tr[-1] - tr[0]
        freq = (n - 1) / duration              # n samples = n - 1 intervals
        print(f"record {i}: {n} samples from {tr[0]:7.3f} to {tr[-1]:7.3f} s, ({duration:.3f}s, {freq:.3f} Hz)")


def plot_record_trajectory(data, records, header, i):
    """Trajectory of record i on the screen: inside in green, outside in red, target as a yellow ring."""
    m = record_mask(data, records[i])
    r_in, r_out = target_radii(header)
    w, h = header["screenWidth"], header["screenHeight"]
    is_in = m & data["inside"]
    is_out = m & ~data["inside"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.add_patch(Rectangle((-w / 2, -h / 2), w, h, fill=False, edgecolor="magenta", label="screen"))
    ax.add_patch(Circle((0, 0), r_out, color="yellow", alpha=0.7, label="target"))   # yellow disk...
    ax.add_patch(Circle((0, 0), r_in, color="white"))                                # ...minus white disk = ring
    ax.plot(data["x"][is_in], data["y"][is_in], ".", color="green", markersize=2, label="inside")
    ax.plot(data["x"][is_out], data["y"][is_out], ".", color="red", markersize=3, label="outside")
    ax.set_xlim(-w / 2 - 50, w / 2 + 50)
    ax.set_ylim(-h / 2 - 50, h / 2 + 50)
    ax.set_aspect("equal")
    ax.set_title(f"record {i}")
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


def plot_record_time_series(data, records, i):
    """x, y and inside flag over time for record i (3 panels sharing the time axis)."""
    m = record_mask(data, records[i])
    t = time_s(data)[m]
    fig, axs = plt.subplots(3, 1, figsize=(7, 6), sharex=True)
    axs[0].plot(t, data["x"][m], ".-", color="blue", linewidth=0.3, label="x")
    axs[0].set_ylabel("X position")
    axs[1].plot(t, data["y"][m], ".-", color="orange", linewidth=0.3, label="y")
    axs[1].set_ylabel("Y position")
    axs[2].plot(t, data["inside"][m].astype(int), ".-", color="green", linewidth=0.3, label="is_inside")
    axs[2].set_ylabel("Is Inside")
    axs[2].set_xlabel("Time (s)")
    for a in axs:
        a.grid(True)
        a.legend()
    plt.tight_layout()
    plt.show()
