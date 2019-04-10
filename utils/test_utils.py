import base64

from utils.adb_utils import run_adb_command


def start_color_test(color):
    command = command_for_color(color)
    run_adb_command(command)


def command_for_color(color):
    html = '<body style="background-color:%s"></body>' % color
    html_b64 = str(base64.b64encode(html.encode("ascii"))).lstrip("b").replace("'", "")

    command = [
        "adb",
        "shell",
        "am start -n org.mozilla.firefox/org.mozilla.gecko.BrowserApp "
        "-a android.intent.action.VIEW "
        """-d "data:text/html;base64,{}" """.format(html_b64)
        + "--ez showstartpane false",
    ]

    return command
