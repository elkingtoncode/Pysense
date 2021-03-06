import subprocess
import unittest

import mock

from hardware.benchmark import disk


FIO_OUTPUT_READ = """MYJOB-fake-disk: (groupid=0, jobs=1): err= 0: pid=5427:
  read : io=123456KB, bw=123456KB/s, iops=123, runt= 10304msec""".splitlines()


@mock.patch.object(subprocess, 'Popen')
class TestBenchmarkDisk(unittest.TestCase):

    def setUp(self):
        super(TestBenchmarkDisk, self).setUp()
        self.hw_data = [('disk', 'fake-disk', 'size', '10'),
                        ('disk', 'fake-disk2', 'size', '15')]

    def test_disk_perf(self, mock_popen):
        mock_popen.return_value = mock.Mock(stdout=FIO_OUTPUT_READ)
        disk.disk_perf(self.hw_data)

        expected = [
            ('disk', 'fake-disk', 'size', '10'),
            ('disk', 'fake-disk2', 'size', '15'),
            ('disk', 'fake-disk', 'standalone_read_1M_KBps', '123456'),
            ('disk', 'fake-disk', 'standalone_read_1M_IOps', '123'),
            ('disk', 'fake-disk', 'standalone_randread_4k_KBps', '123456'),
            ('disk', 'fake-disk', 'standalone_randread_4k_IOps', '123'),
            ('disk', 'fake-disk', 'standalone_read_1M_KBps', '123456'),
            ('disk', 'fake-disk', 'standalone_read_1M_IOps', '123'),
            ('disk', 'fake-disk', 'standalone_randread_4k_KBps', '123456'),
            ('disk', 'fake-disk', 'standalone_randread_4k_IOps', '123'),
            ('disk', 'fake-disk', 'simultaneous_read_1M_KBps', '123456'),
            ('disk', 'fake-disk', 'simultaneous_read_1M_IOps', '123'),
            ('disk', 'fake-disk', 'simultaneous_randread_4k_KBps', '123456'),
            ('disk', 'fake-disk', 'simultaneous_randread_4k_IOps', '123')
        ]
        self.assertEqual(sorted(expected), sorted(self.hw_data))

    def test_get_disks_name(self, mock_popen):
        result = disk.get_disks_name(self.hw_data)
        self.assertEqual(sorted(['fake-disk', 'fake-disk2']), sorted(result))

    def test_run_fio(self, mock_popen):
        mock_popen.return_value = mock.Mock(stdout=FIO_OUTPUT_READ)
        hw_data = []
        disks_list = ['fake-disk', 'fake-disk2']
        disk.run_fio(hw_data, disks_list, "read", 123, 10, 5)

        self.assertEqual(sorted(
            [('disk', 'fake-disk', 'simultaneous_read_123_KBps', '123456'),
             ('disk', 'fake-disk', 'simultaneous_read_123_IOps', '123')]),
            sorted(hw_data))
