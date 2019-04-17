#!/bin/bash

OUTPUT=$1

REFBROW_0320=$2
REFBROW=$3
FENIX=$4
FENNEC=$5
GVE=$6
GVE_0408=$7

python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$REFBROW_0320" --trials 4 --testtime 20 --test-percent-range 70 25
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$REFBROW" --trials 4 --testtime 20 --test-percent-range 70 25
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$FENIX" --trials 4 --testtime 20 --test-percent-range 70 25
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$FENNEC" --trials 4 --testtime 20 --test-percent-range 70 25
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$GVE" --trials 4 --testtime 20 --test-percent-range 70 25
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$GVE_0408" --trials 4 --testtime 20 --test-percent-range 70 25
