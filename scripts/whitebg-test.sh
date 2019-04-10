#!/bin/bash

OUTPUT=$1

REFBROW=$2
FENIX=$3
FENNEC=$4
GVE=$5

COLOR="white"

python3 tests/android_pre_post_color_test.py --ignore-input --color "$COLOR" --output "$OUTPUT" --browser-apk "$REFBROW" --trials 2 --testtime 20 --test-percent-range 100 90
python3 tests/android_pre_post_color_test.py --ignore-input --color "$COLOR" --output "$OUTPUT" --browser-apk "$FENIX" --trials 2 --testtime 20 --test-percent-range 100 90
python3 tests/android_pre_post_color_test.py --ignore-input --color "$COLOR" --output "$OUTPUT" --browser-apk "$FENNEC" --trials 2 --testtime 20 --test-percent-range 100 90
python3 tests/android_pre_post_color_test.py --ignore-input --color "$COLOR" --output "$OUTPUT" --browser-apk "$GVE" --trials 2 --testtime 20 --test-percent-range 100 90
