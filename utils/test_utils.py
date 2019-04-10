import base64

from utils.adb_utils import run_adb_command, get_mozilla_pkgname

PACKAGE_ACTIVITY = {
    'org.mozilla.geckoview_example': 'GeckoViewActivity',
    'org.mozilla.reference.browser': 'BrowserTestActivity',
    'org.mozilla.fenix.browser': 'BrowserTestActivity',
    'org.mozilla.firefox': 'BrowserApp'
}


def start_color_test(color):
    command = command_for_color(color)
    run_adb_command(command)


def command_for_color(color):
    html = '<body style="background-color:%s"></body>' % color
    html_b64 = str(base64.b64encode(html.encode("ascii"))).lstrip("b").replace("'", "")
    pkgname = get_mozilla_pkgname()

    start_cmd = "am start -n {}/{}.{} ".format(
        pkgname, pkgname, PACKAGE_ACTIVITY[pkgname]
    )
    if 'org.mozilla.firefox' in pkgname:
        start_cmd = "am start -n org.mozilla.firefox/org.mozilla.gecko.BrowserApp "

    command = [
        "adb",
        "shell",
        start_cmd
        + "-a android.intent.action.VIEW "
        """-d "data:text/html;base64,{}" """.format(html_b64)
        + "--ez showstartpane false",
    ]

    return command
