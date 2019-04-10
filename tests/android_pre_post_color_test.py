import datetime
import time

from utils.android_parser import AndroidParser
from utils.data_saver import DataSaver
from utils.adb_utils import (
    get_phone_model,
    get_battery_info,
    get_screen_timeout,
    set_screen_timeout,
    install_package,
    uninstall_package,
    parse_battery_info,
    wait_for_drop,
)
from utils.test_utils import start_color_test
from utils.utils import finish_same_line, write_same_line, custom_input

RESOLUTION = 4  # time between data points in seconds


def main(args):
    print("Running Android Pre/Post test.")
    print("Running %s background color test.\n" % args.color)
    print("Make sure you have no extra apps running in the background.")
    print(
        "Make sure that there is a wakelock app running"
        "(if going passed 30 minutes of testing)."
    )
    print("Charging is disabled before the test starts. It is")
    print("enabled automatically when we reach the end of the test.")

    custom_input("Press enter when ready...", args.ignore_input)
    ds = DataSaver(args.output)
    ds.start()

    print("Getting Phone Model...")
    model = get_phone_model()
    print("Is the model %s correct?" % model.model)

    custom_input("Press Enter to confirm...", args.ignore_input)

    print("Disabling charging...")
    model.disable_charging()

    custom_input("Is it disabled?", args.ignore_input)

    old_screentimeout = get_screen_timeout()
    print("Old screen timeout: {}".format(old_screentimeout))
    set_screen_timeout(12000000)

    for trial in range(args.trials):
        print("\nOn trial {} \n".format(str(trial)))

        print("Installing app...")
        if args.browser_apk:
            install_package(args.browser_apk)

        print("Attempting to start %s test..." % args.color)
        start_color_test(args.color)

        custom_input(
            "When the test is ready, start the measurements by pressing enter...",
            args.ignore_input
        )

        print("Waiting for a charge counter drop...")
        wait_for_drop()
        print("Drop detected, starting test")
        print("Start time: {}".format(datetime.datetime.utcnow()))

        info = parse_battery_info(get_battery_info())
        info["timestamp"] = time.time()
        starttime = info["timestamp"]
        ds.add(info, "batterydata")

        print("Starting values:")
        for k, v in info.items():
            print("{}: {}".format(k, v))
        start_cc = int(info["Charge counter"])
        start_pc = int(info["level"])

        currtime = 0
        testtime_seconds = args.testtime * 60
        while currtime - starttime < testtime_seconds:
            time.sleep(RESOLUTION)
            currtime = time.time()
            write_same_line(
                "Elapsed time (seconds): {}".format(str(currtime - starttime))
            )
        finish_same_line()

        info = parse_battery_info(get_battery_info())
        info["timestamp"] = time.time()
        ds.add(info, "batterydata")

        print("End time: {}".format(datetime.datetime.utcnow()))
        print("Final values:")
        for k, v in info.items():
            print("{}: {}".format(k, v))
        end_cc = int(info["Charge counter"])
        end_pc = int(info["level"])

        results = {
            'Charge counter used': start_cc - end_cc,
            'Percent used': start_pc-end_pc
        }
        ds.add(results, "summary{}_".format(str(trial)))

        print("\nCharge counter used: {}".format(
            str(results['Charge counter used'])
        ))
        print("Percent used: {} \n".format(
            str(results['Percent used'])
        ))

    set_screen_timeout(old_screentimeout)
    if args.browser_apk:
        uninstall_package()

    print("Enabling charging...")
    model.enable_charging()

    print("Stopping data saver...")
    ds.stop_running()
    print("Done.")


if __name__ == "__main__":
    parser = AndroidParser().get_parser()
    parser.add_argument(
        "--color", help="Color of background for the test.", required=True
    )
    parser.add_argument(
        "--browser-apk",
        help="If the browser is not installed, provide the path to the APK to install."
             " If none is provided, we assume a single package already exists.",
        default=None
    )
    parser.add_argument(
        "--ignore-input",
        help="If set, skips all requests for input (default is false).",
        action="store_true",
        default=False
    )
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

    args = parser.parse_args()
    main(args)
