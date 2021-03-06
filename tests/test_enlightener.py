"""Test Enlightener module."""

import math
import unittest
import sys
import time

sys.path.append('../enlightener')

from connections import (get_config_for_device,
                         get_device_list,
                         get_status_for_device,
                         update_light_value)
from enlightener import analyze_time_diff
from enlightener import compile_light_time
from enlightener import (get_light_threshold,
                         get_time_diff)
from enlightener import (get_device_ids,
                         update_device_light_thresholds,
                         get_current_light_reading,
                         report_light_threshold_values)
from enlightener import read_write


class TestEnlightener(unittest.TestCase):
    """Test connections."""

    def setUp(self):
        """Set up."""
        self.device1 = '99000512002151'
        self.sheet_values = [
            ['99000512002128', '1'],
            ['99000512000619', '2']
        ]
        self.new_values = [
            ['99000512000621', '256'],
            ['99000512000648', '512']
        ]

        self.test_device_list = ['99000512002128', '99000512000619']

        self.time1 = '2018-06-01 00:00:00'
        self.time2 = '2018-06-01 00:05:00'
        self.time3 = '2018-06-01 00:10:00'
        self.time4 = '2018-06-01 00:15:00'
        self.time5 = '2018-06-01 00:20:00'

    def test_get_light_threshold(self):
        """Test light threshold fetch."""
        comp = compile_light_time(self.device1)
        threshold = comp['light']

        self.assertGreater(
            int(threshold), 0)

    def test_get_device_list(self):
        """Test device list fetch."""
        bool_test = False
        resp = get_device_list()
        mylist = resp['devices']
        test_device_list = self.test_device_list

        for device in test_device_list:
            if device in mylist:
                bool_test = True
        self.assertEqual(bool_test, True)

    def test_analyze_time_diff(self):
        """Test time diff processor."""
        diff1 = get_time_diff(self.time1, self.time2)
        diff2 = get_time_diff(self.time1, self.time3)
        diff3 = get_time_diff(self.time1, self.time4)
        diff4 = get_time_diff(self.time1, self.time5)

        self.assertLessEqual(diff1, 5)
        self.assertLessEqual(diff2, 10)
        self.assertLessEqual(diff3, 15)
        self.assertGreaterEqual(diff3, 15)
        self.assertGreaterEqual(diff4, 20)

    def test_get_light_threshold_set_get(self):
        """Test threshold."""
        device_id = self.device1
        update_light_value(device_id, "1001")
        time.sleep(math.floor(100 / 24))
        req = get_config_for_device(device_id)
        print(req)
        threshold_value = get_light_threshold(req)
        self.assertEqual(threshold_value, '1001')

    def test_get_device_ids(self):
        values = get_device_ids()
        print(values)
        test = False
        if '99000512000647' in values:
            test = True
        elif '99000512000619' in values:
            test = True

        self.assertTrue(test)

    # def test_process_device_ids(self):
    #     """Test the process runner."""
    #     process = process_device_ids()
    #     print('\n')
    #     print(process)
    #     print('\n')
    #     reprocess = process_device_ids()
    #     print('\n')
    #     print(reprocess)
    #     print('\n')

    def test_update_device_light_thresholds(self):
        # update_device_light_thresholds(True)
        read_write("read")

if __name__ == '__main__':
    unittest.main()
