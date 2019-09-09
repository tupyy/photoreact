from django.test import TestCase
from gallery.utils.validate_data import validate_list


class TestUtils(TestCase):

    def test_validate_list(self):
        """
        Description: Convert a list of strings representing ids to int
        API:
        Method:
        Date: 09/09/2019
        User: cosmin
        Expected return code:
        Expected values: list of int
        """
        raw_data = ["1", "2"]
        res = validate_list(raw_data, int)
        for i in res:
            self.assertTrue(isinstance(i, int))

    def test_validate_list2(self):
        """
        Description: Convert a list of strings. Only one entry is valid
        API:
        Method:
        Date: 09/09/2019
        User: cosmin
        Expected return code:
        Expected values: [1]
        """
        raw_data = ["1", "blabla"]
        res = validate_list(raw_data, int)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], 1)

    def test_validate_list3(self):
        """
        Description: provide a string instead of a list. The string is represent an int.
        API:
        Method:
        Date: 09/09/2019
        User: cosmin
        Expected return code:
        Expected values: list of one int
        """
        raw_data = "1"
        res = validate_list(raw_data, int)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], 1)

    def test_validate_list4(self):
        """
        Description: Test with bad input data.
        API:
        Method:
        Date: 09/09/2019
        User: cosmin
        Expected return code:
        Expected values: empty list because second arg is not callable
        """
        raw_data = "1"
        res = validate_list(raw_data, "int")
        self.assertEqual(len(res), 0)

    def test_validate_list5(self):
        """
        Description: Test with bad input data.
        API:
        Method:
        Date: 09/09/2019
        User: cosmin
        Expected return code:
        Expected values: empty list because first arg is not None
        """
        res = validate_list(None, "int")
        self.assertEqual(len(res), 0)
