import subprocess
import time

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
    level = parse_battery_info(get_battery_info())["level"]
    starttime = time.time()
    finish_same_line()
    while not dropped:
        currlevel = parse_battery_info(get_battery_info())["level"]
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


def run_adb_command(command):
    res = subprocess.check_output(command)
    print(res.decode("ascii"))
