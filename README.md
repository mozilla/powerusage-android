# powerusage-android
Mozilla-driven battery and power-usage measurement tools for Android (7,8,9)



[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/powerusage-android/blob/master/LICENSE.txt)
[![Build Status](https://travis-ci.org/mozilla/powerusage-android.svg?branch=master)](https://travis-ci.org/mozilla/powerusage-android)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Preliminary Setup:
1. Your Moto G5 and/or Pixel 2 phone(s) should be rooted and OEM/carrier-unlocked
2. Python 3 is installed and available in your system ```$PATH```
3. git clone your fork of https://github.com/mozilla/powerusage-android
4. ```python3 setup.py develop```

Running a Test:
1. cd into /scripts or just call whichever test you want, like so:
  * ```$ ./scripts/whitebg-test.sh``` 
2. You should now see output similar to https://gist.github.com/stephendonner/9c611a3dfc6d26c4f203bd06b38f688b, the (reverse) gist of which -- pun intended and taken -- is:

```
Running Android Pre/Post test. Running white background color test.

Make sure you have no extra apps running in the background. Make sure that there is a wakelock app running(if going passed 30 minutes of testing). Charging is disabled before the test starts. It is enabled automatically when we reach the end of the test. Getting Phone Model... Is the model Moto_G__5 correct? Disabling charging... Old screen timeout: 12000000

On trial 0

Installing app... Attempting to start white test... Starting: Intent { act=android.intent.action.VIEW dat=data:text/html;base64,PGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6d2hpdGUiPjwvYm9keT4= cmp=org.mozilla.reference.browser/.IntentReceiverActivity (has extras) }
```

followed by the magic and substance of the test/measurements, which are the (many) datapoints, of which we are currently focused on Charge-Counter values, as well as deltas, variance across scenarios, etc:

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
Charge counter: 2627234
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
Charge counter: 2549718
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

Charge counter used: 77516
Percent used: 1 
```
