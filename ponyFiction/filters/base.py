import os
import re
from lxml import etree
from functools import wraps
try:
    from django.conf import settings as django_settings
    django_settings.DEBUG
except ImportError:
    class django_settings:
        DEBUG = False


def load_xslt_transform(file_path):
    with file(file_path, 'rb') as f:
        return etree.XSLT(etree.XML(f.read(), base_url = file_path))
    
def html_doc_transform(fn):
    @wraps(fn)
    def wrapper(doc, **kw):
        if isinstance(doc, basestring):
            doc = etree.HTML(doc or '<body></body>')
        return fn(doc, **kw)
    return wrapper

def html_text_transform(fn):
    @wraps(fn)
    def wrapper(doc):
        if not isinstance(doc, basestring):
            doc = html_doc_to_string(doc)
        return fn(doc)
    return wrapper
    
def transform_xslt_params(kw):
    for key, value in kw.items():
        if isinstance(value, basestring):
            value = etree.XSLT.strparam(value)
        elif type(value) in (int, long, float):
            value = str(value)
        else:
            raise TypeError(key)
        kw[key] = value
    return kw
    
def xslt_transform_loader(file_path):
    dir_path = os.path.dirname(file_path)
    def factory(xslt_name):
        xslt_path = os.path.join(dir_path, xslt_name)
        
        if not django_settings.DEBUG:
            transform_ = load_xslt_transform(xslt_path)
            def transform(doc, **kw):
                kw = transform_xslt_params(kw)
                return transform_(doc, **kw).getroot()
        else:
            def transform(doc, **kw):
                kw = transform_xslt_params(kw)
                transform = load_xslt_transform(xslt_path)
                return transform(doc, **kw).getroot()
        
        return html_doc_transform(transform)
    return factory    
    
def html_doc_to_string(doc):
    body = doc.xpath('//body')
    if len(body) < 1: return ''
    body = body[0]
    doc = ''.join([(body.text or '')] + [etree.tounicode(elem, method='html') for elem in body.getchildren()])
    doc = re.subn(r'&#x([0-9a-fA-F]+);', lambda x: unichr(int(x.groups()[0], 16)), doc)[0]
    return doc 