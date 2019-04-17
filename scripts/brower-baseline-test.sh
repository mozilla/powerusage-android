#!/bin/bash

OUTPUT=$1

REFBROW=$2
FENIX=$3
FENNEC=$4
GVE=$5

python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$REFBROW" --trials 1 --testtime 20 --test-percent-range 100 90
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$FENIX" --trials 1 --testtime 20 --test-percent-range 100 90
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$FENNEC" --trials 1 --testtime 20 --test-percent-range 100 90
python3 tests/android_browser_baseline_test.py --ignore-input --output "$OUTPUT" --browser-apk "$GVE" --trials 1 --testtime 20 --test-percent-range 100 90
