import datetime
import time
import json
import os

from utils.android_parser import AndroidParser
from utils.data_saver import DataSaver
from utils.adb_utils import (
    charge_battery,
    discharge_battery,
    get_phone_model,
    get_battery_info,
    get_battery_level,
    get_screen_timeout,
    initialize_power_measurements,
    finalize_power_measurements,
    set_screen_timeout,
    install_package,
    uninstall_package,
    parse_battery_info,
    wait_for_drop,
)
from utils.test_utils import start_browser
from utils.utils import finish_same_line, write_same_line, custom_input

RESOLUTION = 4  # time between data points in seconds


def main(args):
    print("Running Android Pre/Post test.")
    print("Make sure you have no extra apps running in the background.")
    print(
        "Make sure that there is a wakelock app running"
        "(if going passed 30 minutes of testing)."
    )
    print("Charging is disabled before the test starts. It is")
    print("enabled automatically when we reach the end of the test.")

    custom_input("Press enter when ready...", False)
    ds = DataSaver(args.output)
    ds.start()

    print("Getting Phone Model...")
    model = get_phone_model()
    print("Is the model %s correct?" % model.model)

    custom_input("Press Enter to confirm...", False)

    print("Disabling charging...")
    model.disable_charging()

    custom_input("Is it disabled?", False)

    old_screentimeout = get_screen_timeout()
    print("Old screen timeout: {}".format(old_screentimeout))
    set_screen_timeout(12000000)

    # Ensure that it's sorted from low to high
    args.test_percent_range.sort()

    for trial in range(args.trials):
        currtestname = "%s_%s" % (args.test_name, str(trial))
        currlevel = get_battery_level()
        if currlevel > args.test_percent_range[1]:
            discharge_battery(args.test_percent_range[1], model=model)
        elif currlevel < args.test_percent_range[0]:
            charge_battery(args.test_percent_range[1], model=model)

        print("\nOn trial {} \n".format(str(trial)))

        custom_input(
            "When the test is ready, start the measurements by pressing enter...",
            False
        )

        print("Waiting for a charge counter drop...")
        wait_for_drop()
        print("Drop detected, starting test")
        print("Start time: {}".format(datetime.datetime.utcnow()))

        print("Initializing power measurements")
        initialize_power_measurements(ds.output, currtestname)
        starttime = time.time()

        currtime = 0
        testtime_seconds = args.testtime * 60
        while currtime - starttime < testtime_seconds:
            time.sleep(RESOLUTION)
            currtime = time.time()
            write_same_line(
                "Elapsed time (seconds): {}".format(str(currtime - starttime))
            )
        finish_same_line()

        power_data = finalize_power_measurements(ds.output, args.binary_name, currtestname)
        print("Power data (in perfherder format):")
        print("PERFHERDER_DATA: %s" % str(power_data))

        filepath = os.path.join(
            ds.output, 'perfherder_data_%s.json' % currtestname
        )
        print("\nSaving perfherder data to %s" % filepath)
        with open(filepath, 'w') as f:
            json.dump(power_data, f, indent=4)

    set_screen_timeout(old_screentimeout)

    print("Enabling charging...")
    model.enable_charging()

    print("Stopping data saver...")
    ds.stop_running()
    print("Done.")


if __name__ == "__main__":
    parser = AndroidParser().get_parser()
    parser.add_argument(
        "--testtime",
        help="Time to run test for (in minutes, default is 1).",
        default=1,
        type=float
    )
    parser.add_argument(
        '--trials',
        help='Number of trials to run (default is 1).',
        default=1,
        type=int
    )
    parser.add_argument(
        '--test-percent-range',
        help="Range of battery percent to test in (default is 90-100%).",
        default=[90, 100],
        nargs='+',
        type=int
    )
    parser.add_argument(
        '--test-name',
        help="Name of the test (used to name perfherder data).",
        required=True,
        type=str
    )
    parser.add_argument(
        '--binary-name',
        help="Binary name of the browser in testing. i.e. org.mozilla.geckoview_example. "
        "Used for parsing power measurements.",
        required=True,
        type=str
    )

    args = parser.parse_args()
    main(args)
