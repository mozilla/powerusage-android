import subprocess
import time
import re
import os

from utils.utils import write_same_line, finish_same_line


class PhoneModel:
    def __init__(self, model):
        self.model = model
        self.disable_command = ""
        self.enable_command = ""

    def disable_charging(self):
        disable_charging(model=self)

    def enable_charging(self):
        enable_charging(model=self)


class PixelPhone(PhoneModel):
    def __init__(self, model):
        super(PixelPhone, self).__init__(model)
        self.disable_command = (
            "'echo 1 > /sys/class/power_supply/battery/input_suspend'"
        )
        self.enable_command = "'echo 0 > /sys/class/power_supply/battery/input_suspend'"


class MotoG5Phone(PhoneModel):
    def __init__(self, model):
        super(MotoG5Phone, self).__init__(model)
        self.disable_command = (
            "'echo 0 > /sys/class/power_supply/battery/charging_enabled'"
        )
        self.enable_command = (
            "'echo 1 > /sys/class/power_supply/battery/charging_enabled'"
        )


MODELS = {"Pixel_2": PixelPhone, "Moto_G__5": MotoG5Phone}


def get_phone_model():
    res = subprocess.check_output(["adb", "devices", "-l"]).decode("ascii")
    for modelname in MODELS:
        if modelname in res:
            return MODELS[modelname](modelname)
    raise Exception("Could not find a PhoneModel for: %s" % model)


def get_default_phone_model():
    return PixelPhone("Pixel_2")


def get_screen_timeout():
    res = subprocess.check_output(
        ["adb", "shell", "settings", "get", "system", "screen_off_timeout"]
    )
    return res.decode('ascii').strip('\n')


def set_screen_timeout(timeout):
    subprocess.check_output(
        [
            "adb",
            "shell",
            "settings",
            "put",
            "system",
            "screen_off_timeout",
            str(timeout)
        ]
    )


def get_mozilla_packages():
    return subprocess.check_output(
        ["adb", "shell", "pm", "list", "packages", "mozilla"]
    )


def get_mozilla_pkgname():
    # There should only be one package
    res = get_mozilla_packages()
    pkgname = res.decode('ascii').split(":")[-1].strip('\n')
    return pkgname


def close_package(pkgname):
    subprocess.check_output(["adb", "shell", "am", "force-stop", pkgname])


def install_package(path_to_apk):
    try:
        uninstall_existing()

        res = subprocess.check_output(["adb", "install", "-r", "-g", path_to_apk])
        print(res)

        pkgname = get_mozilla_pkgname()
        if pkgname == 'org.mozilla.firefox':
            # Start it once and then close it
            print("Starting browser for welcome page...")
            subprocess.check_output(
                [
                    "adb",
                    "shell",
                    "am start -n org.mozilla.firefox/org.mozilla.gecko.BrowserApp"
                ]
            )
            time.sleep(10)
            close_package(pkgname)

    except Exception as e:
        if "ALREADY_EXISTS" in str(e):
            print("Package already exists.")
        else:
            raise


def uninstall_package(app=None):
    if not app:
        app = get_mozilla_pkgname()

    subprocess.check_output(["adb", "uninstall", app])


def uninstall_existing():
    packages = get_mozilla_packages().decode('ascii')
    pkglist = packages.split('\n')
    for pkgname in pkglist:
        if pkgname == '':
            continue
        pkgname = pkgname.split(':')[-1]
        print("Uninstalling {}...".format(pkgname))
        uninstall_package(app=pkgname)


def disable_charging(model=None):
    if not model:
        model = get_default_phone_model()

    subprocess.check_output(["adb", "shell", "su -c %s" % model.disable_command])


def enable_charging(model=None):
    if not model:
        model = get_default_phone_model()

    subprocess.check_output(["adb", "shell", "su -c %s" % model.enable_command])


def get_battery_info():
    res = subprocess.check_output(["adb", "shell", "dumpsys", "battery"])
    return res


def get_battery_level():
    return int(parse_battery_info(get_battery_info())["level"])


def parse_battery_info(batinfo):
    """
	Parses an entry such as:
		Current Battery Service state:
		AC powered: false\n
		USB powered: true\n
		Wireless powered: false\n
		Max charging current: 3000000\n
		Max charging voltage: 5000000\n
		Charge counter: 3991656\n
		status: 2\n
		health: 2\n
		present: true\n
		level: 96\n
		scale: 100\n
		voltage: 4387\n
		temperature: 300\n
		technology: Li-ion\n

	"""
    info = {}
    lines = batinfo.decode("ascii").split("\n")
    for line in lines[1:]:  # Ignore the first line
        if line == "":
            continue
        name, val = line.split(":")
        name = name.strip()
        val = val.strip()
        info[name] = val
    return info


def wait_for_drop():
    dropped = False
    level = parse_battery_info(get_battery_info())["Charge counter"]
    starttime = time.time()
    finish_same_line()
    while not dropped:
        currlevel = parse_battery_info(get_battery_info())["Charge counter"]
        if level != currlevel:
            dropped = True
            break
        time.sleep(5)
        currtime = time.time()
        write_same_line(
            "Time elapsed waiting for drop: {} seconds".format(
                str(currtime - starttime)
            )
        )
    finish_same_line()


def discharge_battery(targetlevel, currlevel=None, model=None):
    if not model:
        model = get_default_phone_model()

    if not currlevel:
        currlevel = get_battery_level()

    model.disable_charging()  # In case it wasn't already disabled
    while currlevel != targetlevel:
        wait_for_drop()
        currlevel = get_battery_level()
        write_same_line(
            "Discharging to {}, currently at {}".format(
                str(targetlevel), str(get_battery_level())
            )
        )
    finish_same_line()


def charge_battery(targetlevel, model=None):
    if not model:
        model = get_default_phone_model()

    currlevel = get_battery_level()
    decrease = False
    if currlevel == targetlevel:
        discharge_battery(currlevel - 1, currlevel=currlevel, model=model)
        currlevel = get_battery_level()

    print("Started charging...")
    model.enable_charging()
    while currlevel < targetlevel:
        time.sleep(5)
        currlevel = get_battery_level()
        write_same_line(
            "Charging to {}, curently at {}".format(str(targetlevel), str(currlevel))
        )
    finish_same_line()

    print("Finished charging, disabling it now...")
    model.disable_charging()


def run_adb_command(command, print_return=True):
    res = subprocess.check_output(command)
    if print_return:
        print(res.decode("ascii"))
    return res.decode("ascii")

def shell_output(command):
    adb_command = ["adb", "shell"]
    split_command = command.split(" ")
    adb_command.extend(split_command)

    res = run_adb_command(adb_command, print_return=False)
    return res


def initialize_power_measurements(output_dir, test_name):
    # Set the screen brightness to ~50% for consistency of measurements across
    # devices
    shell_output("settings put system screen_brightness 127")
    shell_output("dumpsys batterystats --reset")
    shell_output("dumpsys batterystats --enable full-wake-history")

    filepath = os.path.join(output_dir, "%s_battery-before.txt" % test_name)
    with open(filepath, "w") as output:
        output.write(shell_output("dumpsys battery"))


def finalize_power_measurements(output_dir, binary, test_name, os_baseline=False):
    filepath = os.path.join(output_dir, "%s_battery-after.txt" % test_name)
    with open(filepath, "w") as output:
        output.write(shell_output("dumpsys battery"))
    filepath = os.path.join(output_dir, "%s_batterystats.csv" % test_name)
    with open(filepath, "w") as output:
        output.write(shell_output("dumpsys batterystats --checkin"))
    filepath = os.path.join(output_dir, "%s_batterystats.txt" % test_name)
    with open(filepath, "w") as output:
        batterystats = shell_output("dumpsys batterystats")
        output.write(batterystats)

    # Get the android version
    android_version = shell_output(
        "getprop ro.build.version.release"
    ).strip()
    major_android_version = int(android_version.split('.')[0])

    estimated_power = False
    uid = None
    total = cpu = wifi = smearing = screen = proportional = 0
    full_screen = 0
    full_wifi = 0
    re_uid = re.compile(r'proc=([^:]+):"%s"' % binary)
    re_wifi = re.compile(r'.*wifi=([\d.]+).*')
    re_cpu = re.compile(r'.*cpu=([\d.]+).*')
    re_estimated_power = re.compile(r"\s+Estimated power use [(]mAh[)]")
    re_proportional = re.compile(r"proportional=([\d.]+)")
    re_screen = re.compile(r"screen=([\d.]+)")
    re_full_screen = re.compile(r"\s+Screen:\s+([\d.]+)")
    re_full_wifi = re.compile(r"\s+Wifi:\s+([\d.]+)")

    re_smear = re.compile(r".*smearing:\s+([\d.]+)\s+.*")
    re_power = re.compile(
        r"\s+Uid\s+\w+[:]\s+([\d.]+) [(]([\s\w\d.\=]*)(?:([)] "
        r"Including smearing:.*)|(?:[)]))"
    )

    batterystats = batterystats.split("\n")
    for line in batterystats:
        if uid is None and not os_baseline:
            # The proc line containing the Uid and app name appears
            # before the Estimated power line.
            match = re_uid.search(line)
            if match:
                print("matched")
                uid = match.group(1)
                re_power = re.compile(
                    r"\s+Uid %s[:]\s+([\d.]+) [(]([\s\w\d.\=]*)(?:([)] "
                    r"Including smearing:.*)|(?:[)]))" % uid
                )
                continue
        if not estimated_power:
            # Do not attempt to parse data until we have seen
            # Estimated Power in the output.
            match = re_estimated_power.match(line)
            if match:
                estimated_power = True
            continue
        if full_screen == 0:
            match = re_full_screen.match(line)
            if match and match.group(1):
                full_screen += float(match.group(1))
                continue
        if full_wifi == 0:
            match = re_full_wifi.match(line)
            if match and match.group(1):
                full_wifi += float(match.group(1))
                continue
        if re_power:
            match = re_power.match(line)
            if match:
                ttotal, breakdown, smear_info = match.groups()
                total += float(ttotal) if ttotal else 0

                cpu_match = re_cpu.match(breakdown)
                if cpu_match and cpu_match.group(1):
                    cpu += float(cpu_match.group(1))

                wifi_match = re_wifi.match(breakdown)
                if wifi_match and wifi_match.group(1):
                    wifi += float(wifi_match.group(1))

                if smear_info:
                    # Smearing and screen power are only
                    # available on android 8+
                    smear_match = re_smear.match(smear_info)
                    if smear_match and smear_match.group(1):
                        smearing += float(smear_match.group(1))
                    screen_match = re_screen.search(line)
                    if screen_match and screen_match.group(1):
                        screen += float(screen_match.group(1))
                    prop_match = re_proportional.search(smear_info)
                    if prop_match and prop_match.group(1):
                        proportional += float(prop_match.group(1))
        if full_screen and full_wifi and (cpu and wifi and smearing or total):
            # Stop parsing batterystats once we have a full set of data.
            # If we are running an OS baseline, stop when we've exhausted
            # the list of entries.
            if not os_baseline:
                break
            elif line.replace(' ', '') == '':
                break

    cpu = total if cpu == 0 else cpu
    screen = full_screen if screen == 0 else screen
    wifi = full_wifi if wifi == 0 else wifi

    if os_baseline:
        uid = 'all'
    print(
        "power data for uid: %s, cpu: %s, wifi: %s, screen: %s, proportional: %s"
        % (uid, cpu, wifi, screen, proportional)
    )

    # Send power data directly to the control-server results handler
    # so it can be formatted and output for perfherder ingestion

    power_data = {
        "type": "power",
        "test": test_name,
        "unit": "mAh",
        "values": {
            "cpu": float(cpu),
            "wifi": float(wifi),
            "screen": float(screen),
        },
    }

    if major_android_version >= 8:
        power_data['values']['proportional'] = float(proportional)

    return power_data
