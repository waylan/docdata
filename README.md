DocData
=======

A better Meta-Data handler for lightweight markup languages.

Currently, DocData supports MultiMarkdown style meta-data and YAML meta-data.
While those meta-data formats are generally used in Markdown documents, DocData
can work with any lightweight markup language as long as the document begins with
an appropriately formatted meta-data section.

Note that DocData does not detect the style of meta-data used within a document.
You need to know ahead of time which format is used and call the appropriate
parser.  Additionally, each parser will return the meta-data in a format unique to
that format, so ensure that your code works with the format you have chosen.

The parser for each format will strip the meta-data from the document. At that
point you can forward the document on to your lightweight markup processor of
choice. You might even want to use some the meta-data to configure the behavior
of your lightweight markup processor.

YAML Meta-Data
--------------

Given a document that contains YAML style meta-data, simply pass it to
the `docdata.yamldata.get_data` function:

```python
from docdata.yamldata import get_data

doc, data = get_data(doc)
```

The `docdata.yamldata.get_data` function will return a tuple which contains the
document with the meta-data removed and the meta-data as returned by the YAML
parser. Note that if the YAML root data structure parsed by YAML is not a
dictionary, it is assumed that no data is defined, the YAML block is not
removed from the document, and an empty dict is returned as data.

As YAML provides for and recognizes various types out-of-the-box, no additional
features need to be provided. The document can now be passed to your lightweight
markup processor of choice.

MultiMarkdown Meta-Data
-----------------------

Given a document that contains MultiMarkdown style meta-data, simply pass it to
the `docdata.mmddata.get_data` function:

```python
from docdata.mmddata import get_data

doc, data = get_data(doc)
```

The `docdata.mmddata.get_data` function will return a tuple which contains the
document with the meta-data removed and the meta-data as a Python dictionary.
Now the document can be passed to your lightweight markup processor of choice.

### Transformations

Unlike other meta-data formats (such as YAML), MultiMarkdown style meta-data
makes no assumptions about the types of the various values in the meta-data.
In fact, each line of the data for a given key is an item in a list. Even
a single line of meta-data results in a list with one item in it, each item
being a string. To make your data more useful, DocData allows you to define
transformations for various known keys in your meta-data.

You can define the transformations as callables which accept a value and
return a transformed value and register them by using the
`docdata.mmddata.transformer` decorator:

```python
from docdata.mmddata import get_data, transformer
from datetime import datetime

@transformer('date')
def date(value):
    "Convert string (in YYYY/MM/DD format) to a datetime.datetime object. "
    return datetime.strptime(value[0], '%Y/%m/%d')

doc, data = get_data(doc)
```

Notice that the string `'date'` was passed to the `docdata.mmddata.transformer`
decorator as the "key". That "key" corresponds to the key used in the meta-data.
Therefore, the following meta-data would result in a `datetime.datetime` object
being returned as the value of the 'date' key:

```
---
Title: Some Title
Date: 2015/03/05
---
```

Note that with the above document, no transformer was defined for the "title" key.
In that case, the title was passed through unaltered. However, you can define a
default transformer for all unspecified keys. If you don't assign a key when
registering a transformer, then that transformer is used as the default:

```python
@transformer()      # <= No key assigned here
def default(value):
    "The default transformer. "
    return ' '.join(value)
```

### Collection Isolation

In the above examples, the transformers did not need to be passed to the
meta-data parser. Still, `docdata.mmddata.get_data` did the right thing.
This is because, behind the scenes, a global instance of a
`docdata.mmddata.TransformerCollection` was defined within the `docdata.mmddata`
module, and the `docdata.mmddata.transformer` decorator registers transformers
with that collection.

However, if you need to use unique collections of transformers (perhaps per
request and/or per thread), you can create your own
`docdata.mmddata.TransformerCollection` instance and work with that instance.
In fact, the `TransformerCollection.register` method is a decorator you
can use to register a transformer with a specific instance:

```python
from docdata.mmddata import get_data, TransformerCollection

mytc = TransformerCollection()

@mytc.register()
def default(value):
    return ' '.join(value)

doc, data = get_data(doc, mytc)
```

Note that `docdata.mmddata.get_data` accepts a second optional argument, which
must be an instance of the `docdata.mmddata.TransformerCollection` class.

You can also pass in a dictionary of transformers when you create an instance
of a `docdata.mmddata.TransformerCollection`:

```python
tc = TransformerCollection(
    items={
        'author': (lambda v: v[0].upper()),
        'summary': (lambda v: '\n'.join(v)),
        'tags': (lambda v: v)
    },
    default=(lambda v: ' '.join(v))
)
```

Note that the "default" transformer must be assigned outside of the dictionary
so that it is still possible to define a "default" key if necessary. This
example is also interesting as each of the transformers are defined as
lambda functions. A transformer can be any callable which accepts one argument
and returns an object.

### Raw Data

If you would like the raw data without any transformations, you can use the
`docdata.mmddata.get_raw_data` function. It simply accepts a document and
returns a document and a dictionary of raw data :

```python
from docdata.mmddata import get_data

doc, data = get_raw_data(doc)
```

While the `docdata.mmddata.get_data` function with no transformers defined would
accomplish the same thing, using `docdata.mmddata.get_raw_data` should be slightly
faster as it is unnecessary to iterate over the items and pass each one through
a dummy, do-nothing transformer.
