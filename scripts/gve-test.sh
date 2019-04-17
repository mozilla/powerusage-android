#!/bin/bash

OUTPUT=$1

GVE=$2

#python3 tests/android_pre_post_color_test.py --ignore-input --color "white" --output "$OUTPUT" --browser-apk "$GVE" --trials 2 --testtime 20 --test-percent-range 100 90
#python3 tests/android_pre_post_color_test.py --ignore-input --color "red" --output "$OUTPUT" --browser-apk "$GVE" --trials 1 --testtime 20 --test-percent-range 100 90
python3 tests/android_pre_post_color_test.py --ignore-input --color "black" --output "$OUTPUT" --browser-apk "$GVE" --trials 1 --testtime 20 --test-percent-range 100 90
#python3 tests/android_pre_post_color_test.py --ignore-input --color "green" --output "$OUTPUT" --browser-apk "$GVE" --trials 1 --testtime 20 --test-percent-range 100 90
#python3 tests/android_pre_post_color_test.py --ignore-input --color "blue" --output "$OUTPUT" --browser-apk "$GVE" --trials 1 --testtime 20 --test-percent-range 100 90
