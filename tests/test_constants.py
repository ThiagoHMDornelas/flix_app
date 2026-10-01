from unittest import TestCase

from constants import NATIONALITY_CHOICES, NATIONALITY_DISPLAY


class ConstantsTestCase(TestCase):
    def test_nationality_display_is_reverse_of_choices(self):
        expected = {code: name for name, code in NATIONALITY_CHOICES.items()}

        self.assertEqual(NATIONALITY_DISPLAY, expected)
