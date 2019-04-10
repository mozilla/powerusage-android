import datetime
import time

from utils.android_parser import AndroidParser
from utils.data_saver import DataSaver
from utils.adb_utils import (
    get_phone_model,
    get_battery_info,
    parse_battery_info,
    wait_for_drop,
)
from utils.utils import finish_same_line, write_same_line

RESOLUTION = 4  # time between data points in seconds
TESTTIME = 1  # minutes


def main(args):
    OUTPUT = args.output

    print("Running Android Pre/Post test.")
    print("Make sure you have no extra apps running in the background.")
    print(
        "Make sure that there is a wakelock app running"
        "(if going passed 30 minutes of testing)."
    )
    print("Charging is disabled before the test starts. It is")
    print("enabled automatically when we reach the end of the test.")

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

    input("When the test is ready, start the recording by pressing enter...")

    print("Waiting for a percentage drop...")
    # wait_for_drop()
    print("Drop detected, starting test")
    print("Start time: {}".format(datetime.datetime.utcnow()))

    info = parse_battery_info(get_battery_info())
    info["timestamp"] = time.time()
    starttime = info["timestamp"]
    ds.add(info, "batterydata")

    print("Starting values:")
    for k, v in info.items():
        print("{}: {}".format(k, v))

    currtime = 0
    testtime_seconds = TESTTIME * 60
    while currtime - starttime < testtime_seconds:
        time.sleep(5)
        currtime = time.time()
        write_same_line("Elapsed time (seconds): {}".format(str(currtime - starttime)))
    finish_same_line()

    info = parse_battery_info(get_battery_info())
    info["timestamp"] = time.time()
    ds.add(info, "batterydata")

    print("End time: {}".format(datetime.datetime.utcnow()))
    print("Final values:")
    for k, v in info.items():
        print("{}: {}".format(k, v))

    print("Enabling charging...")
    model.enable_charging()

    print("Stopping data saver...")
    ds.stop_running()
    print("Done.")


if __name__ == "__main__":
    args = AndroidParser().parse_args()
    main(args)
