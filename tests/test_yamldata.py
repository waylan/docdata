import unittest
import datetime
from docdata import yamldata

class TestYamlData(unittest.TestCase):
    def test_yaml_data(self):
        doc = '''---
Author: John Doe
Date: 2015-05-08 14:15:16
Integer: 0x2A
---

Document content.
'''
        self.assertEqual(
            yamldata.get_data(doc),
            (
                'Document content.\n',
                {
                    'Author': 'John Doe',
                    'Date': datetime.datetime(2015, 5, 8, 14, 15, 16),
                    'Integer': 42
                }
            )
        )

    def test_end_deliminator(self):
        doc = '''---
Author: John Doe
Date: 2015-05-08
Integer: 42
...
Document content.
'''
        self.assertEqual(
            yamldata.get_data(doc),
            (
                'Document content.\n',
                {
                    'Author': 'John Doe',
                    'Date': datetime.date(2015, 5, 8),
                    'Integer': 42
                }
            )
        )

    def test_bad_deliminator(self):
        doc = '''---
Author: John Doe
Date: 2015-05-08
Integer: 42
-.-
Document content.
'''
        self.assertEqual(
            yamldata.get_data(doc),
            (doc, {})
        )

    def test_blank_first_line(self):
        doc = '''
---
Author: John Doe
Date: 2015-05-08
Integer: 42
---
Document content.
'''
        self.assertEqual(
            yamldata.get_data(doc),
            (doc, {})
        )

    def test_bad_yaml(self):
        doc = '''---
foo
...
Document content.
'''
        self.assertEqual(
            yamldata.get_data(doc),
            (doc, {})
        )

    def test_no_yaml(self):
        doc = 'Document content.'
        self.assertEqual(
            yamldata.get_data(doc),
            (doc, {})
        )