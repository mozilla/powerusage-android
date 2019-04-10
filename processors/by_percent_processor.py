import os
import json
import numpy as np
from matplotlib import pyplot as plt

from utils.utils import get_paths_from_dir

RESULTSDIR = "/home/sparky/Documents/mozwork/osbaseline1554005928"
MAXPC = 100
MINPC = 5


def get_battery_data(datadir):
    files = get_paths_from_dir(datadir, file_matchers=["ttimes_pc_"])
    data = {}

    print("Opening JSONs, found {}".format(len(files)))
    for file in files:
        with open(file, "r") as f:
            name = file.split("breakdown_")[1].split("155")[0]
            data[name] = json.load(f)["trial-times"]
    print(data)
    return data


def main():
    batdata = get_battery_data(RESULTSDIR)

    ordering = [
        "100-90",
        "90-80",
        "80-70",
        "70-60",
        "60-50",
        "50-40",
        "40-30",
        "30-20",
        "20-10",
        "15-5",
    ]
    stddevs = []
    means = []
    for pcrange in ordering:
        means.append(np.mean(batdata[pcrange]))
        stddevs.append(np.std(batdata[pcrange]))

    pc_stds = []
    for i, el in enumerate(means):
        pc_stds.append(100 * (stddevs[i] / el))
    print(pc_stds)

    plt.figure()
    plt.bar(np.arange(len(means)), means, yerr=stddevs)
    plt.xticks(np.arange(len(ordering)), ordering)
    plt.title("Mean time to drain through percent range")
    plt.xlabel("Percent range")
    plt.ylabel("Mean time")
    plt.show()


if __name__ == "__main__":
    main()
