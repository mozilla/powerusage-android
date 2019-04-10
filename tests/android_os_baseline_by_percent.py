import os
import datetime
import time

from utils.android_parser import AndroidParser
from utils.data_saver import DataSaver
from utils.adb_utils import (
    charge_battery,
    discharge_battery,
    get_phone_model,
    get_battery_info,
    get_battery_level,
    parse_battery_info,
    wait_for_drop,
)
from utils.utils import finish_same_line, write_same_line

RESOLUTION = 4  # time between data points in seconds

# start percent is exclusive, end percent is inclusive
PERCENT_INTERVALS = [
    # (100, 90),
    # (90, 80),
    # (80, 70),
    # (70, 60),
    # (60, 50),
    (50, 40),
    (40, 30),
    (30, 20),
    (20, 10),
    (15, 5),
]
TRIALS = 10


def main(args):
    OUTPUT = args.output

    print("Running OS baseline (percent-split) test.\n")
    print("Make sure you have no apps running in the background.")
    print("Make sure that there is a wakelock app running.")
    print(
        "Charging is disabled and enabled periodically throughout "
        "the tests to gather {} trials for {} percentage ranges.".format(
            str(TRIALS), str(len(PERCENT_INTERVALS))
        )
    )

    _ = input("Press enter when ready...")
    ds = DataSaver(OUTPUT)
    ds.start()

    print("Getting Phone Model...")
    model = get_phone_model()
    print("Is the model %s correct?" % model.model)
    input("Press Enter to confirm...")

    print("Disabling charging...")
    model.disable_charging()
    input("Is it disabled?")

    for startpercent, endpercent in PERCENT_INTERVALS:
        print("\nOn percent interval: {} to {}".format(startpercent, endpercent))
        trialtimes = []
        for trialnum in range(TRIALS):
            print(
                "\nRunning trial {}, current times are {}".format(
                    trialnum, str(trialtimes)
                )
            )
            print("Start time: {}".format(datetime.datetime.utcnow()))
            info = parse_battery_info(get_battery_info())
            if int(info["level"]) <= startpercent:
                charge_battery(startpercent, model=model)
            elif int(info["level"]) > startpercent:
                discharge_battery(startpercent, model=model)

            dname = "pc_breakdown_{}-{}-{}".format(startpercent, endpercent, trialnum)
            outputdir = os.path.join(ds.output, dname)
            os.mkdir(outputdir)

            starttime = time.time()

            try:
                level = 1000
                prevcharge = 0
                prevlevel = 0
                prevtemp = 0
                while level > endpercent:  # end percent is inclusive
                    start = time.time()

                    info = parse_battery_info(get_battery_info())
                    info["timestamp"] = time.time()
                    ds.add(info, os.path.join(dname, "batterydata"))
                    level = int(info["level"])

                    if (
                        prevcharge != info["Charge counter"]
                        or prevlevel != level
                        or prevtemp != info["temperature"]
                    ):
                        finish_same_line()
                    write_same_line(
                        "{} | Current capacity: {}%, {}, Temp: {}".format(
                            datetime.datetime.utcnow(),
                            str(level),
                            info["Charge counter"],
                            info["temperature"],
                        )
                    )

                    prevlevel = level
                    prevcharge = info["Charge counter"]
                    prevtemp = info["temperature"]

                    end = time.time()
                    telapsed = end - start

                    if telapsed < RESOLUTION:
                        time.sleep(RESOLUTION - telapsed)
            except Exception as e:
                model.enable_charging()
                raise

            endtime = time.time()
            trialtimes.append(endtime - starttime)

            finish_same_line()

        print(
            "Trial times for {} to {}: {}".format(
                startpercent, endpercent, str(trialtimes)
            )
        )

        ds.add(
            {"trial-times": trialtimes},
            "ttimes_pc_breakdown_{}-{}".format(startpercent, endpercent),
        )

    print("Enabling charging...")
    model.enable_charging()

    print("Stopping data saver...")
    ds.stop_running()
    print("Done.")


if __name__ == "__main__":
    args = AndroidParser().parse_args()
    main(args)
