import unittest

from watcher import StoppableThread


class StoppableThreadTestCase(unittest.TestCase):
    def test_stoppable_thread(self):
        thread = StoppableThread(None, None)
        self.assertTrue(thread, 'thread should have been created')
        self.assertFalse(thread.isAlive(), 'thread should not be alive')
        thread.start()
        self.assertTrue(thread.isAlive(), 'thread should be alive')
        thread.stop()
        thread.join(0.1)
        self.assertFalse(thread.isAlive(), 'thread should not be alive')


if __name__ == '__main__':
    unittest.main()
