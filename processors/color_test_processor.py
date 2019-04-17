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
PIXELDIR = "/home/sparky/Documents/mozwork/weekend-run"
MOTODIR = "/home/sparky/Documents/mozwork/motog5-powertests"
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
    colors = ['black-bg', 'white-bg', 'green-bg', 'red-bg']
    #colors = ['browser-baseline']
    browsers = ['refbrow', 'fenix', 'fennec', 'gve']
    #browsers = ['refbrow-0320', 'refbrow', 'fenix', 'fennec', 'gve', 'gve-0408']
    browsers2 = ['refbrow', 'fenix', 'fennec', 'gve']
    line_colors = {
        'white-bg': 'silver',
        'black-bg': 'black',
        'red-bg': 'red',
        'blue-bg': 'blue',
        'green-bg': 'green',
        'browser-baseline': 'orange'
    }

    p2_batdata = {}
    for color in colors:
        print("On color: %s" % color)
        p2_batdata[color] = {}
        for browser in browsers:
            print("On browser: %s" % browser)
            p2_batdata[color][browser] = get_battery_data(
                os.path.join(PIXELDIR, color, browser),
                ['summary']
            )

    
    mg5_batdata = {}
    for color in colors:
        mg5_batdata[color] = {}
        for browser in browsers2:
            mg5_batdata[color][browser] = get_battery_data(
                os.path.join(MOTODIR, color, browser),
                ['summary']
            )
    

    sum_line_p2 = [0 for _ in browsers]

    plt.figure()
    all_p2_lines = {}
    all_mg5_lines = {}
    x_range = np.arange(len(browsers))
    for i, color in enumerate(colors):
        plt.subplot(2,3,i+1)
        plt.title(color)
        if i in (0,3,):
            plt.ylabel("Charge counters used (a.u.)")
        if i in (3,4,):
            plt.xlabel("Browser")

        line_p2 = []
        line_mg5 = []
        for i, browser in enumerate(browsers):
            line_p2.append(p2_batdata[color][browser]['Charge counter'])
            if color in ('red-bg', 'blue-bg', 'green-bg'):
                sum_line_p2[i] += line_p2[-1] * 0.78
            line_mg5.append(mg5_batdata[color][browser]['Charge counter'])

        mincc = min(line_p2)
        maxcc = max(line_p2)
        new_line_p2 = line_p2

        '''
        new_line_p2 = []
        for el in line_p2:
            new_line_p2.append((((el - mincc) * (100)) / (maxcc - mincc)))
        '''
        if color not in all_p2_lines:
            all_p2_lines[color] = []
        if color not in all_mg5_lines:
            all_mg5_lines[color] = []
        all_p2_lines[color].append(new_line_p2)
        all_mg5_lines[color].append(line_mg5)

        plt.plot(x_range, new_line_p2, color=line_colors[color])
        plt.plot(x_range, line_mg5, color=line_colors[color], linestyle='--')
        plt.xticks(x_range, browsers)

    '''
    maxcc = 0
    mincc = 999999999999999
    for color in colors:
        tmpmax = max(all_p2_lines[color][0])
        tmpmin = min(all_p2_lines[color][0])
        if tmpmax > maxcc:
            maxcc = tmpmax
        if tmpmin < mincc:
            mincc = tmpmin

    print(maxcc)
    print(mincc)

    all_p2_lines_new = {}
    for color in colors:
        new_line_p2 = []
        line_p2 = all_p2_lines[color][0]
        for el in line_p2:
            new_line_p2.append((((el - mincc) * (100)) / (maxcc - mincc)))
        if color not in all_p2_lines_new:
            all_p2_lines_new[color] = []
        all_p2_lines_new[color].append(new_line_p2)
    all_p2_lines = all_p2_lines_new
    print("here")
    '''
    plt.figure()
    plt.title("All browsers")
    plt.ylabel("Charge counters used (a.u.)")
    plt.xlabel("Browsers")
    for color in colors:
        for line in all_mg5_lines[color]:
            plt.plot(x_range, line, color=line_colors[color], linestyle='--')
        for line in all_p2_lines[color]:
            plt.plot(x_range, line, color=line_colors[color])

    #plt.plot(x_range, [x-33000 for x in sum_line_p2], color='purple', label='Weighted sum of RGB power consumption')
    plt.xticks(x_range, browsers)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()
 