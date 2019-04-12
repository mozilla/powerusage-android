# powerusage-android

<h2>Mozilla-driven battery and power-usage measurement tools for Android (7,8).</h2>

🔥🦊⏱

## (The) More stuff You should Know 🌈⭐

* Test Plan: [Android Power/Battery-Use](https://docs.google.com/document/d/1r1J_BZnE5l8nXoLVXVR1hUlEkzaPX2gx_ueZABkzi6g/edit) (Google Doc, WIP)
* Main bug: [bug 1511350](https://bugzilla.mozilla.org/show_bug.cgi?id=1511350) - Test impact of dark mode on power usage
* Builds atop Bob Clary's work with Rob Wood on [power.py](https://searchfox.org/mozilla-central/rev/b3ac60ff061c7891e77c26b73b61804aa1a8f682/testing/raptor/raptor/power.py)
* Raptor power-testing code refactoring needed to quickly abstract and extend supported testing capabilities ([bug 1534778](https://bugzilla.mozilla.org/show_bug.cgi?id=1534778) 'quick' first step)

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/powerusage-android/blob/master/LICENSE.txt)
[![Build Status](https://travis-ci.org/mozilla/powerusage-android.svg?branch=master)](https://travis-ci.org/mozilla/powerusage-android)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Preliminary Setup:
1. Your **Moto G5** ([unlock](https://accounts.motorola.com/ssoauth/login?TARGET=https://motorola-global-portal.custhelp.com/cc/cas/sso/redirect/standalone%2Fbootloader%2Funlock-your-device-b), [specs](https://www.gsmarena.com/motorola_moto_g5-8454.php)) and/or **Pixel 2** [unlock](https://www.androidcentral.com/how-root-google-pixel-2)[specs](https://www.gsmarena.com/google_pixel_2-8733.php) phones should be *rooted* and *OEM/carrier-unlocked* (further [unlocking docs](https://docs.google.com/document/d/1XQLtvVM2U3h1jzzzpcGEDVOp4jMECsgLYJkhCfAwAnc/edit)
2. [**Python 3.7.3**](https://www.python.org/downloads/release/python-373/) is installed and available in your system ```$PATH```
3. You have [**git**](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed and configured, also available in your system ```$PATH```
4. [**adb**](https://www.xda-developers.com/quickly-install-adb/) is installed and available in your system ```$PATH``` (if ```adb devices``` doesn't spit out errors, you should be good to go)
5. ```git clone``` your fork of https://github.com/mozilla/powerusage-android (read-only would be: ```git clone https://github.com/mozilla/powerusage-android```)
6. ```cd powerusage-android```
7. ```python3 setup.py develop```:
```
$ python3 setup.py develop
```
```
running develop
running egg_info
writing powerusage_android.egg-info/PKG-INFO
writing dependency_links to powerusage_android.egg-info/dependency_links.txt
writing top-level names to powerusage_android.egg-info/top_level.txt
reading manifest file 'powerusage_android.egg-info/SOURCES.txt'
writing manifest file 'powerusage_android.egg-info/SOURCES.txt'
running build_ext
Creating /usr/local/lib/python3.7/site-packages/powerusage-android.egg-link (link to .)

Installed /Users/stephendonner/powerusage-android
Processing dependencies for powerusage-android==0.1.0
Finished processing dependencies for powerusage-android==0.1.0
```
## Test-Environment (Device) Cleanup
## Uninstall Browser Apps
**Manually:** tap and hold until you can drag to the Uninstall option at the top right) all of your current Firefox-based browser apps (Fennec, GeckoView Example [GVE], Fenix, and Reference Browser [RefBrow]).

## Install Browser APKs:
I will prettify this later, but here are my (Stephen) build sources, for my Moto G5, running Android 7.x:
* Fennec (Firefox 64.0.2): https://archive.mozilla.org/pub/mobile/releases/64.0.2/android-api-16/en-US/fennec-64.0.2.en-US.android-arm.apk
* RefBrow: https://index.taskcluster.net/v1/task/project.mobile.reference-browser.signed-nightly.nightly.2019.4.9.latest/artifacts/public/target.arm.apk
* Fenix: https://index.taskcluster.net/v1/task/project.mobile.fenix.signed-nightly.nightly.2019.4.9.latest/artifacts/public/target.arm.apk
* GVE: https://taskcluster-artifacts.net/dzV5pl0SRz6IvbIDR1TEIA/0/public/build/geckoview_example.apk

(Greg can add his here too if so desired)

## Running a Test:
1. For each color's power test, you must ```mkdir [unique name]``` with a convention of your choosing; ```black-bg```, ```white-bg```, etc.
2. From the top-level (root) dir, run (e.g. substituting values, where appropriate):
   ```$ ./scripts/blackbg-test.sh --output black-bg ```
    Ensure that your custom dir exists prior to the above test run; ```results``` or similar, will do, for our purposes.
3. You should now see output similar to https://gist.github.com/stephendonner/9c611a3dfc6d26c4f203bd06b38f688b:


Here's a sample "batch" test of colors, called eye_of_sauron.py:

```
#!/bin/bash 

scripts/blackbg-test.sh black-bg fennec-64.0.2.en-US.android-arm.apk refbrow-target.arm.apk target.arm.apk geckoview_example.apk
scripts/whitebg-test.sh white-bg fennec-64.0.2.en-US.android-arm.apk refbrow-target.arm.apk target.arm.apk geckoview_example.apk
scripts/redbg-test.sh red-bg fennec-64.0.2.en-US.android-arm.apk refbrow-target.arm.apk target.arm.apk geckoview_example.apk
scripts/greenbg-test.sh green-bg fennec-64.0.2.en-US.android-arm.apk refbrow-target.arm.apk target.arm.apk geckoview_example.apk
scripts/bluebg-test.sh blue-bg fennec-64.0.2.en-US.android-arm.apk refbrow-target.arm.apk target.arm.apk geckoview_example.apk

```

Note: at the time of this doc update, ```greenbg-test.sh``` and ```bluebg-test.sh``` are not in-tree, and are used to test locally and here for illustrative purposes.

We'll soon be moving to Raptor proper, to hook into All the Things™ we need for capabilities of all types.


```
Running Android Pre/Post test. Running white background color test.

Make sure you have no extra apps running in the background. Make sure that there is a wakelock app running(if going passed 30 minutes of testing). Charging is disabled before the test starts. It is enabled automatically when we reach the end of the test. Getting Phone Model... Is the model Moto_G__5 correct? Disabling charging... Old screen timeout: 12000000

On trial 0

Installing app... Attempting to start white test... Starting: Intent { act=android.intent.action.VIEW dat=data:text/html;base64,PGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6d2hpdGUiPjwvYm9keT4= (forced wrap here for illustration)
cmp=org.mozilla.reference.browser/.IntentReceiverActivity (has extras) }
```

followed by the magic and substance of the test/measurements, which are the (many) datapoints, of which we are currently focused on Charge-Counter values (**Charge counter: 267234**), as well as deltas, variance across scenarios, etc:

```
Waiting for a charge counter drop...

Time elapsed waiting for drop: 35.473793029785156 seconds
Drop detected, starting test
Start time: 2019-04-10 23:06:34.454324
Starting values:
AC powered: false
USB powered: false
Wireless powered: false
MOD powered: false
Max charging current: 0
Max charging voltage: 0
**Charge counter: 2627234**
status: 3
health: 2
present: true
level: 94
scale: 100
voltage: 4242
temperature: 297
technology: Li-ion
mod level: -1
mod status: 1
mod flag: 0
mod type: 0
timestamp: 1554937594.504281
Elapsed time (seconds): 1200.3231749534607
End time: 2019-04-10 23:26:34.919007
Final values:
AC powered: false
USB powered: false
Wireless powered: false
MOD powered: false
Max charging current: 0
Max charging voltage: 0
**Charge counter: 2549718**
status: 3
health: 2
present: true
level: 93
scale: 100
voltage: 4220
temperature: 315
technology: Li-ion
mod level: -1
mod status: 1
mod flag: 0
mod type: 0
timestamp: 1554938794.918973

**Charge counter used: 77516**
**Percent used: 1**
```
