import unittest

from watcher import Watcher, StoppableThread


class WatcherTestCase(unittest.TestCase):
    def callback(self, message):
        self.message = message
        return message

    def setUp(self):
        self.watcher = Watcher(self.callback)
        self.message = ''

    def test_callback(self):
        self.assertEqual(self.watcher.callback, self.callback,
                         'watcher.callback != callback')
        message = 'test message'
        self.watcher.callback(message)
        self.assertEqual(message, self.message,
                         'callback didn\'t return same message')

    def test_scan_directories_no_match(self):
        self.watcher.directories = list()
        self.watcher.files = list()
        self.watcher._scan_directories()
        self.assertFalse(self.watcher._scan_results,
                         '_scan_results should be empty')

    def test_scan_directories_match(self):
        self.watcher.directories = ['.', 'tests']
        self.watcher.files = ['txt']
        self.watcher._scan_directories()
        self.assertTrue(self.watcher._scan_results,
                        '_scan_results should not be empty')
        self.assertIn('tests\\ascii_encoded.txt',
                      self.watcher._scan_results.keys())
        self.assertIn('tests\\utf-16_encoded.txt',
                      self.watcher._scan_results.keys())

    def test_scan_files_no_match(self):
        self.message = ''
        self.watcher.directories = ['.', 'tests']
        self.watcher.files = ['txt']
        self.watcher._scan_directories()
        self.assertTrue(self.watcher._scan_results, 'missing scan results')
        self.watcher._scan_files()
        self.assertEqual(self.message, '',
                         'message should not have been modified')

    def test_scan_files_match(self):
        self.message = ''
        self.watcher.directories = ['.', 'tests']
        self.watcher.files = ['txt']
        self.watcher._scan_directories()
        self.assertTrue(self.watcher._scan_results, 'missing scan results')
        self.assertIn('tests\\ascii_encoded.txt',
                      self.watcher._scan_results.keys())
        with open('tests/ascii_encoded.txt', 'a') as file:
            file.write('extra line')
        self.watcher._scan_files()
        self.assertEqual(self.message, 'extra line',
                         'message should have been modified')

    def test_stop_monitor(self):
        thread = StoppableThread(None, None)
        self.watcher._monitor_thread = thread
        self.watcher._scan_thread = thread
        thread.start()
        self.assertTrue(self.watcher._monitor_thread.isAlive(),
                        'thread should be alive')
        self.assertTrue(self.watcher._scan_thread.isAlive(),
                        'thread should be alive')
        self.watcher.stop_monitor()
        self.assertFalse(self.watcher._monitor_thread.isAlive(),
                         'thread should not be alive')
        self.assertFalse(self.watcher._scan_thread.isAlive(),
                         'thread should not be alive')


if __name__ == '__main__':
    unittest.main()
