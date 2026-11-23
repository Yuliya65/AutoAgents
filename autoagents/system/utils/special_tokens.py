import unittest
from autoagents.system.utils.special_tokens import MSG_SEP, FILENAME_CODE_SEP

class TestSpecialTokens(unittest.TestCase):
    def test_special_tokens_exist_and_are_strings(self):
        self.assertIsInstance(MSG_SEP, str)
        self.assertIsInstance(FILENAME_CODE_SEP, str)

    def test_special_tokens_not_empty(self):
        self.assertTrue(len(MSG_SEP) > 0)
        self.assertTrue(len(FILENAME_CODE_SEP) > 0)

    def test_special_tokens_are_distinct(self):
        self.assertNotEqual(MSG_SEP, FILENAME_CODE_SEP)

    def test_expected_token_values(self):
        self.assertEqual(MSG_SEP, "#*000*#")
        self.assertEqual(FILENAME_CODE_SEP, "#*001*#")

if __name__ == "__main__":
    unittest.main()