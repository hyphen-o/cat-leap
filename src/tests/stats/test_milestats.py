import unittest
import json
import sys

sys.path.append("../../")

from catleap.stats import MileStastics
from tests.constants import path, expect


class TestFunc(unittest.TestCase):
    def test_get_length(self):
        self.__Ms = MileStastics()

        # BASICからDEVELOPING以上に習熟した場合のテスト
        json_file = open(path.BAS_TO_DEV + "out.json", "r")
        bas_to_dev = json.load(json_file)
        json_file.close()
        expected_length_list = expect.MILE_STATS["length"]["bas_to_dev"]["list"]
        expected_length_mean = expect.MILE_STATS["length"]["bas_to_dev"]["mean"]
        self.__Ms.set_data(bas_to_dev)
        actual_length = self.__Ms.get_length()
        self.assertEqual(expected_length_list, actual_length.list)
        self.assertEqual(expected_length_mean, actual_length.mean)

        # DEVELOPINGからMASTERに習熟した場合のテスト
        json_file = open(path.DEV_TO_MAS + "out.json", "r")
        dev_to_mas = json.load(json_file)
        json_file.close()
        expected_length_list = expect.MILE_STATS["length"]["dev_to_mas"]["list"]
        expected_length_mean = expect.MILE_STATS["length"]["dev_to_mas"]["mean"]
        self.__Ms.set_data(dev_to_mas)
        actual_length = self.__Ms.get_length()
        self.assertEqual(expected_length_list, actual_length.list)
        self.assertEqual(expected_length_mean, actual_length.mean)
    
    def test_get_duplication(self):
        self.__Ms = MileStastics()

        json_file = open(path.BAS_TO_DEV + "dupli.json", "r")
        bas_to_dev = json.load(json_file)
        json_file.close()
        expected_duplication = expect.MILE_STATS["duplication"]["bas_to_dev"]
        self.__Ms.set_data(bas_to_dev)
        actual_duplication = self.__Ms.get_duplication()
        self.assertEqual(expected_duplication, actual_duplication)



if __name__ == "__main__":
    unittest.main()
