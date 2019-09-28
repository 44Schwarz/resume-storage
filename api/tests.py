import unittest
from django.test import TestCase


# Create your tests here.
class TestParseText(unittest.TestCase):
    def test_regex(self):
        import re
        from .tasks import RE_PATTERN

        test_string = 'A-B Company (04/30/1111-07/26/2222; laboris nisi ut aliquipc,fdmf2f ea commodo conse).'

        match = re.findall(RE_PATTERN, test_string)
        if match:
            self.assertEqual(match, [('A-B Company', '04/30/1111', '07/26/2222',
                                      'laboris nisi ut aliquipc,fdmf2f ea commodo conse')])
