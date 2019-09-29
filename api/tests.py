import unittest
from django.test import TestCase


# Create your tests here.
class TestParseText(unittest.TestCase):
    def test_regex(self):
        import re
        from .tasks import RE_PATTERN

        test_string = 'A-B Company (2015-01-11 - 2018-07-26; laboris nisi ut aliquipc,fdmf2f ea commodo conse).'

        match = re.findall(RE_PATTERN, test_string)
        if match:
            self.assertEqual(match, [('A-B Company', '2015-01-11', '2018-07-26',
                                      'laboris nisi ut aliquipc,fdmf2f ea commodo conse')])
