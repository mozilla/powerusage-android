import os
from sys import stdout
from time import sleep

# Write to the same line dynamically with this.
# Call finish_same_line() when you're done with the line.
def write_same_line(x, sleep_time=0.01):
    stdout.write("\r%s" % str(x))
    stdout.flush()
    sleep(sleep_time)


def finish_same_line():
    stdout.write("\r\r\n")


def pattern_find(srcf_to_find, sources):
    if sources is None:
        return True

    for srcf in sources:
        if srcf in srcf_to_find:
            return srcf
    return None


def get_paths_from_dir(source_dir, file_matchers=None):
    paths = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if pattern_find(file, file_matchers):
                paths.append(os.path.join(root, file))
    return paths
