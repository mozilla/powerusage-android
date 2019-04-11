import os
import json
import numpy as np
from matplotlib import pyplot as plt

from utils.utils import get_paths_from_dir

'''
    Expecting the following directory strucuture:
        PIXELDIR/MOTODIR:
            white-bg:
                refbrow
                fenix
                fennec
                gve
            red-bg:
                refbrow
                fenix
                fennec
                gve
            black-bg:
                refbrow
                fenix
                fennec
                gve
'''
PIXELDIR = "/home/sparky/Documents/mozwork/osbaseline1553960001"
MOTODIR = "/home/sparky/Documents/mozwork/osbaseline1553960001"
MAXPC = 100
MINPC = 90


def get_battery_data(datadir, file_matchers=None):
    files = get_paths_from_dir(datadir, file_matchers=file_matchers)
    data = []

    print("Opening JSONs, found {}".format(len(files)))
    for file in files:
        with open(file, "r") as f:
            data.append(json.load(f))

    fmt_data = {}
    fmt_data["level"] = []
    fmt_data["Charge counter"] = []

    for datapoint in data:
        fmt_data["level"].append(int(datapoint["Percent used"]))
        fmt_data["Charge counter"].append(int(datapoint["Charge counter used"]))

    fmt_data["level"] = np.mean(fmt_data["level"])
    fmt_data["Charge counter"] = np.mean(fmt_data["Charge counter"])

    return fmt_data


def main():
    colors = ['white-bg', 'black-bg', 'red-bg']
    browsers = ['refbrow', 'fenix', 'fennec', 'gve']
    line_colors = {
        'white-bg': 'silver',
        'black-bg': 'black',
        'red-bg': 'red'
    }

    p2_batdata = {}
    for color in colors:
        p2_batdata[color] = {}
        for browser in browsers:
            p2_batdata[color][browser] = get_battery_data(
                os.path.join(PIXELDIR, color, browser),
                ['summary']
            )

    mg5_batdata = {}
    for color in colors:
        mg5_batdata[color] = {}
        for browser in browsers:
            mg5_batdata[color][browser] = get_battery_data(
                os.path.join(MOTODIR, color, browser)
            )

    plt.figure()
    all_p2_lines = {}
    all_mg5_lines = {}
    x_range = np.arange(len(browsers))
    for i, color in enumerate(colors):
        plt.subplot(2,2,i+1)
        if i in (0,1):
            plt.title(color + ' - solid is Pixel2, dashed is MotoG5')
        else:
            plt.title(color)
        if i in (0,2,):
            plt.ylabel("Charge counters used (a.u.)")
        if i in (2,3,):
            plt.xlabel("Browser")

        line_p2 = []
        line_mg5 = []
        for browser in browsers:
            line_p2.append(p2_batdata[color][browser])
            line_mg5.append(p2_batdata[color][browser])

        if color not in all_p2_lines:
            all_p2_lines[color] = []
        if color not in all_mg5_lines:
            all_mg5_lines[color] = []
        all_p2_lines[color].append(line_p2)
        all_mg5_lines[color].append(line_mg5)

        plt.plot(x_range, line_p2, color=line_colors[color])
        plt.plot(x_range, line_mg5, color=line_colors[color], linestyle='--')

    plt.subplot(2,2,4)
    plt.title("All colors overlayed")
    plt.xlabel("Browsers")
    for color in colors:
        for line in all_mg5_lines[color]:
            plt.plot(x_range, line, color=line_colors[color], linestyle='--')
        for line in all_p2_lines[color]:
            plt.plot(x_range, line, color=line_colors[color])

    plt.show()


if __name__ == "__main__":
    main()
