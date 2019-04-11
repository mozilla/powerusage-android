# powerusage-android
Mozilla-driven battery and power-usage measurement tools for Android (7,8,9)


[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/powerusage-android/blob/master/LICENSE.txt)
[![Build Status](https://travis-ci.org/mozilla/powerusage-android.svg?branch=master)](https://travis-ci.org/mozilla/powerusage-android)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

**Preliminary Setup:**
1. Your **Moto G5** and/or **Pixel 2** phone(s) should be *rooted* and *OEM/carrier-unlocked* (we have -- scattered? -- docs, which I'll bring back or link to, here)
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
powerusage-android 0.1.0 is already the active version in easy-install.pth

Installed /Users/stephendonner/powerusage-android
Processing dependencies for powerusage-android==0.1.0
Finished processing dependencies for powerusage-android==0.1.0
```

**Running a Test:**
1. ```$ cd scripts``` or just call whichever test you want, from the top-level (root) dir, like so:
   ```$ ./scripts/whitebg-test.sh --output [name of dir]```
    Ensure that your custom dir exists prior to the above test run; ```results``` or similar, will do, for our purposes.
2. You should now see output similar to https://gist.github.com/stephendonner/9c611a3dfc6d26c4f203bd06b38f688b:

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
