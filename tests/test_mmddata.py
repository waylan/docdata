import unittest

from docdata import mmddata

class TestBuildCollection(unittest.TestCase):
    def setUp(self):
        mmddata.tc._registery = {}
        mmddata.tc.default = (lambda v: v)
    
    def test_build_global_collection(self):
        @mmddata.transformer()
        def default(value):
            return ' '.join(value)
        
        @mmddata.transformer('summary')
        def summary(value):
            return '\n'.join(value)
        
        self.assertEqual(len(mmddata.tc._registery.items()), 1)
        self.assertEqual(mmddata.tc.default, default)
        self.assertEqual(mmddata.tc._registery['summary'], summary)
    
    def test_build_collection_instance(self):
        tc = mmddata.TransformerCollection()
        @tc.register()
        def default(value):
            return ' '.join(value)
        
        @tc.register('summary')
        def summary(value):
            return '\n'.join(value)
        
        self.assertEqual(len(tc._registery.items()), 1)
        self.assertEqual(tc.default, default)
        self.assertEqual(tc._registery['summary'], summary)
    
    def test_build_collection_init(self):
        def default(value):
            return ' '.join(value)
        
        def summary(value):
            return '\n'.join(value)
        
        def title(value):
            return value[0].upper()
        
        tc = mmddata.TransformerCollection(
            items={'summary': summary, 'title': title},
            default=default
        )
        self.assertEqual(len(tc._registery.items()), 2)
        self.assertEqual(tc.default, default)
        self.assertEqual(tc._registery['summary'], summary)
        self.assertEqual(tc._registery['title'], title)

class TestCollectionTransform(unittest.TestCase):
    def setUp(self):
        self.tc = mmddata.TransformerCollection(
            items={
                'author': (lambda v: v[0].upper()),
                'summary': (lambda v: '\n'.join(v)),
                'tags': (lambda v: v)
            },
            default=(lambda v: ' '.join(v))
        )
        self.data = {
            'author': ['Bob', 'Jane'],
            'summary': ['foo', 'bar'],
            'tags': ['foo', 'bar'],
            'unknown': ['foo', 'bar']
        }
    
    def test_transform(self):
        self.assertEqual(
            self.tc.transform('author', self.data['author']),
            'BOB'
        )
        self.assertEqual(
            self.tc.transform('summary', self.data['summary']),
            'foo\nbar'
        )
        self.assertEqual(
            self.tc.transform('tags', self.data['tags']),
            ['foo', 'bar']
        )
        self.assertEqual(
            self.tc.transform('unknown', self.data['unknown']),
            'foo bar'
        )
    
    def test_transform_dict(self):
        self.assertEqual(
            self.tc.transform_dict(self.data),
            {
                'author': 'BOB',
                'summary': 'foo\nbar',
                'tags': ['foo', 'bar'],
                'unknown': 'foo bar'
            }
        )
        
class TestDataParser(unittest.TestCase):
    def setUp(self):
        # Deliminated doc
        self.ddoc = """---
Title: Foo Bar
Author: John
Summary: Line one
    Line two
Tags: foo,bar
---

Doc body
"""
        # Non deliminated doc
        self.ndoc = self.ddoc.replace('---\n', '')
        
        self.tc = mmddata.TransformerCollection(
            items={
                'author': (lambda v: v[0].upper()),
                'summary': (lambda v: '\n'.join(v)),
                'tags': (lambda v: v[0].split(','))
            },
            default=(lambda v: ' '.join(v))
        )
    
    def test_deliminated_raw_data(self):
        self.assertEqual(
            mmddata.get_raw_data(self.ddoc),
            (
                'Doc body\n',
                {
                    'title': ['Foo Bar'],
                    'author': ['John'],
                    'summary': ['Line one', 'Line two'],
                    'tags': ['foo,bar']
                }
            )
        )
    
    def test_nondeliminated_raw_data(self):
        self.assertEqual(
            mmddata.get_raw_data(self.ndoc),
            (
                'Doc body\n',
                {
                    'title': ['Foo Bar'],
                    'author': ['John'],
                    'summary': ['Line one', 'Line two'],
                    'tags': ['foo,bar']
                }
            )
        )
    
    def test_get_data(self):
        self.assertEqual(
            mmddata.get_data(self.ddoc, self.tc),
            (
                'Doc body\n',
                {
                    'title': 'Foo Bar',
                    'author': 'JOHN',
                    'summary': 'Line one\nLine two',
                    'tags': ['foo', 'bar']
                }
            )
        )