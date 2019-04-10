import os
import json
import time
from threading import Thread

SAVERINTERVAL = 5  # seconds


class DataSaver(Thread):
    def __init__(self, output):
        Thread.__init__(self)
        self.output = os.path.join(output, "osbaseline" + str(int(time.time())))
        os.mkdir(self.output)
        self.queue = []
        self.stop = False

    def add(self, info, name):
        if not self.stop:
            self.queue.append({"info": info, "name": name})

    def stop_running(self):
        self.stop = True
        while self.queue:
            print("{} items left in queue".format(str(len(self.queue))))
            time.sleep(SAVERINTERVAL)

    def run(self):
        while (not self.stop) or self.queue:
            if not self.queue:
                time.sleep(SAVERINTERVAL)
                continue
            el = self.queue.pop(0)
            with open(
                os.path.join(self.output, el["name"] + str(int(time.time())) + ".json"),
                "w+",
            ) as f:
                json.dump(el["info"], f)
