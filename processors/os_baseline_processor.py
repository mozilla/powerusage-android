import os
import json
import numpy as np
from matplotlib import pyplot as plt

from utils.utils import get_paths_from_dir

RESULTSDIR = "/home/sparky/Documents/mozwork/osbaseline1553960001"
MAXPC = 100
MINPC = 5


def get_battery_data(datadir):
    files = get_paths_from_dir(datadir)
    data = []

    print("Opening JSONs, found {}".format(len(files)))
    for file in files:
        with open(file, "r") as f:
            data.append(json.load(f))

    fmt_data = {}
    fmt_data["level"] = []
    fmt_data["Charge counter"] = []
    fmt_data["times"] = []

    newdata = {}
    for entry in data:
        newdata[entry["timestamp"]] = entry

    for key in sorted(newdata):
        fmt_data["level"].append(int(newdata[key]["level"]))
        fmt_data["Charge counter"].append(int(newdata[key]["Charge counter"]))
        fmt_data["times"].append(float(key))

    return fmt_data


def get_steps(data):
    steps = []
    currpoint = data[0]
    stepcount = 0
    for el in data:
        if el == currpoint:
            stepcount += 1
        else:
            steps.append(stepcount * 4)
            stepcount = 0
            currpoint = el
    return steps


def main():
    batdata = get_battery_data(RESULTSDIR)

    leveldata = batdata["level"]
    ccounterdata = batdata["Charge counter"]
    times = batdata["times"]

    # Change the range for the Charge counter
    tmp = []
    maxcc = ccounterdata[0]
    mincc = ccounterdata[-1]

    for el in ccounterdata:
        tmp.append((((el - mincc) * (MAXPC - MINPC)) / (maxcc - mincc)) + MINPC)

    zcount = 0
    for i in leveldata:
        if i == 100:
            zcount += 1
        else:
            break

    plt.title(
        "Charge counter (normalized to range [5%, 100%]) & Percent level over time"
    )
    plt.plot(times, tmp, label="Charge counter")
    plt.plot(times, leveldata, label="Percent Level")
    plt.plot(
        times,
        [p for p in np.arange(MINPC, MAXPC, step=(MAXPC - MINPC) / len(times))][::-1],
        label="Straight line",
    )
    plt.plot(
        times[zcount:],
        [
            p
            for p in np.arange(MINPC, MAXPC, step=(MAXPC - MINPC) / len(times[zcount:]))
        ][::-1],
        label="Straight line",
    )
    plt.xlabel("Time (seconds)")
    plt.ylabel("Percent capacity remaining")
    hlines = [100, 80, 60, 40, 20, 0]
    for el in hlines:
        plt.axhline(y=el, linestyle="--", color="black")
    plt.legend()

    plt.figure()
    steps_level = get_steps(leveldata)
    steps_cc = get_steps(tmp)

    x_range = np.arange(MINPC, MAXPC, step=(MAXPC - MINPC) / len(steps_cc))[::-1]
    plt.plot(x_range, steps_cc, label="Charge counter")

    x_range = np.arange(MINPC, MAXPC, step=(MAXPC - MINPC) / len(steps_level))[::-1]
    plt.plot(x_range, steps_level, label="Percent level")

    plt.title("Time until next percent, or counter drop")
    plt.xlabel("Battery Percent Level")
    plt.ylabel("Time until next drop (seconds)")
    plt.legend()
    plt.axvline(x=80, color="black", linestyle="--")
    plt.axvline(x=70, color="black", linestyle="--")

    plt.show()


if __name__ == "__main__":
    main()
