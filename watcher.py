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
    def __init__(self, frame, directories=[], files=[], keywords=[''],
                 ignore=[]):
        self._frame = frame
        self.directories = list(directories)
        self.files = list(files)
        self.keywords = list(keywords)
        self.ignore = list(ignore)
        self._monitor_thread = None
        self._scan_thread = None
        self._scan_results = dict()
        # This flag, when set, prevents files from being scanned while
        # directories are scanned and lists are renewed.
        self._scan_in_progress = False

    def _scan_directories(self):
        self._scan_in_progress = True
        self._scan_results = dict()
        if not self.directories or not self.files:
            return
        for directory in self.directories:
            with os.scandir(directory) as it:
                for e in it:
                    if e.is_file() and any(n in e.name for n in self.files):
                        self._scan_results[e.path] = e.stat().st_size
        # Eve uses buffered logging which is flushed rarely or upon file
        # access. During scandir above we triggered actual writings to the
        # files and need second stat call to get actual file size.
        for path, size in self._scan_results.items():
            current_size = os.stat(path).st_size
            self._scan_results[path] = current_size
        self._scan_in_progress = False

    def _scan_files(self):
        if self._scan_in_progress:
            return
        if not self.directories or not self.files:
            return
        messages = list()
        for path, size in self._scan_results.items():
            try:
                current_size = os.stat(path).st_size
                if current_size > size:
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
            # ShowBalloon is for windows only. If support for other platforms
            # needed, uncomment popup lines and comment out ShowBalloon line.
            # popup = wx.adv.NotificationMessage('Feven Intel', message)
            # popup.Show(timeout=5)
            self._frame.tb_icon.ShowBalloon('Feven Interl', message, 5000)

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
        # Let's check files for changes every two seconds(timeout=2).
        self._monitor_thread = StoppableThread(
            target=self._scan_files, timeout=2)
        self._monitor_thread.start()
        # Let's scan folders for changes every twelve seconds(timeout=12).
        self._scan_thread = StoppableThread(
            target=self._scan_directories, timeout=12)
        self._scan_thread.start()

    def stop_monitor(self):
        if self._monitor_thread and self._monitor_thread.isAlive():
            self._monitor_thread.stop()
            self._monitor_thread.join(0.05)
        if self._scan_thread and self._scan_thread.isAlive():
            self._scan_thread.stop()
            self._scan_thread.join(0.05)
