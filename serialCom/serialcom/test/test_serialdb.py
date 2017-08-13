#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from .. import serialdb


class TestSerialdb(unittest.TestCase):

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_insert_productItem(self):
        barcode="123456789qwe"
        tight_torque="qwertyuiop"
        tight_angle="asdfghjkkl"
        serialdb.insert_productItem(barcode, tight_torque, tight_angle)
        
    def test_query_productItem(self):
        pass

    def test_query_productInfo(self):
        res = serialdb.query_productInfo()
        if res is None:
            assertEqual(res, None)
        else:
            assertTrue(isinstance(res, dict))


# if __name__ == "__main__":
#     unittest.main()