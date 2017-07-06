import os
import codecs
import threading

import wx.adv


class StoppableThread(threading.Thread):
    def __init__(self, target, timeout):
        super(StoppableThread, self).__init__()
        self._target = target
        self._timeout = timeout
        self._stop_event = threading.Event()

    def run(self):
        while not self.stopped():
            self._stop_event.wait(self._timeout)  # instead of sleeping
            if self.stopped():
                continue
            self._target()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.isSet()


class Watcher:
    # Empty string in keywords means to grab any changes in files.
    def __init__(self, directories=[], files=[], keywords=[''], ignore=[]):
        self.directories = list(directories)
        self.files = list(files)
        self.keywords = list(keywords)
        self.ignore = list(ignore)
        self._monitor_continously = False
        self._monitor_thread = None
        self._scan_results = dict()

    def stop_monitor(self):
        if self._monitor_thread and self._monitor_thread.isAlive():
            self._monitor_continously = False
            self._monitor_thread.stop()
            self._monitor_thread.join(0.05)

    def _scan_directories(self):
        self._scan_results = dict()
        if not self.directories or not self.files:
            return
        for directory in self.directories:
            with os.scandir(directory) as it:
                for e in it:
                    if e.is_file() and any(n in e.name for n in self.files):
                        self._scan_results[e.path] = e.stat().st_size

    def update(self, directories, files, keywords, ignore):
        self.stop_monitor()
        self.directories = list(directories)
        self.files = list(files)
        self.keywords = list(keywords) if keywords else ['']
        self.ignore = list(ignore)
        self._scan_directories()
        self.run_monitor()

    def run_monitor(self):
        self.stop_monitor()
        # Let's check files for changes every second(timeout=1).
        self._monitor_thread = StoppableThread(
            target=self.monitor_once, timeout=1)
        self._monitor_thread.start()

    def monitor_once(self):
        print(threading.enumerate())
        if not self.directories or not self.files:
            return
        messages = list()
        for path, size in self._scan_results.items():
            try:
                current_size = os.stat(path).st_size
                if current_size > size:
                    print(path, current_size, size)
                    with codecs.open(path, 'r', 'utf-16') as file:
                        file.seek(size)
                        lines = file.readlines()
                        match = filter(
                            lambda x: any(e.lower() in x.lower() for e in
                                          self.keywords),
                            lines
                        )
                        for m in match:
                            messages.append(m)
                    self._scan_results[path] = current_size
            except FileNotFoundError:
                del self._scan_results[path]
        if messages:
            message = '\n'.join(messages)
            popup = wx.adv.NotificationMessage('Feven Intel', message)
            popup.Show(timeout=5)
