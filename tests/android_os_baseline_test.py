import datetime
import time

from utils.android_parser import AndroidParser
from utils.data_saver import DataSaver
from utils.adb_utils import get_phone_model, get_battery_info, parse_battery_info
from utils.utils import finish_same_line, write_same_line

RESOLUTION = 4  # time between data points in seconds
SAVERINTERVAL = 5  # seconds
FINALLEVEL = 5


def main(args):
    OUTPUT = args.output

    print("Running OS baseline test.\n")
    print("Make sure you have no apps running in the background.")
    print("Make sure that there is a wakelock app running.")
    print("Charging is disabled at the beginning of the test")
    print("and then enabled when we reach 5%.")

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
    print("Start time: {}".format(datetime.datetime.utcnow()))

    try:
        level = 1000
        prevcharge = 0
        prevlevel = 0
        prevtemp = 0
        while level != FINALLEVEL:
            start = time.time()

            info = parse_battery_info(get_battery_info())
            info["timestamp"] = time.time()
            ds.add(info, "batterydata")
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

    finish_same_line()

    print("Enabling charging...")
    model.enable_charging()

    print("Stopping data saver...")
    ds.stop_running()
    print("Done.")


if __name__ == "__main__":
    args = AndroidParser().parse_args()
    main(args)
