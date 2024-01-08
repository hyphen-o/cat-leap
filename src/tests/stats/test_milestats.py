import unittest
import json
import sys

sys.path.append("../../")

from catleap.stats import MileStastics
from tests.constants import path


class TestFunc(unittest.TestCase):
    def test_get_length(self):
        self.__Ms = MileStastics()

        # BASICからDEVELOPING以上に習熟した場合のテスト
        json_file = open(path.BAS_TO_DEV + "out.json", "r")
        bas_to_dev = json.load(json_file)
        json_file.close()
        expected_length = [14, 4]
        self.__Ms.set_data(bas_to_dev)
        actual_length = self.__Ms.get_length()
        self.assertEqual(expected_length, actual_length)

         # DEVELOPINGからMASTERに習熟した場合のテスト
        json_file = open(path.DEV_TO_MAS + "out.json", "r")
        dev_to_mas = json.load(json_file)
        json_file.close()
        expected_length = [3, 7]
        self.__Ms.set_data(dev_to_mas)
        actual_length = self.__Ms.get_length()
        self.assertEqual(expected_length, actual_length)


if __name__ == "__main__":
    unittest.main()
