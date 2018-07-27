import pyinotify
import time
import os

class ProcessTransientFile(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        line = file.readline()
        if line:
            print(line)

filename = './test.txt'
file = open(filename,'r')
#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.watch_transient_file(filename, pyinotify.IN_MODIFY, ProcessTransientFile)

notifier.loop()