from django.conf import settings
from django.utils.importlib import import_module

_formats = None
def list_formats():
    global _formats
    if _formats is None:
        _formats = list(iter_formats())
    return _formats

def iter_formats():
    for name in settings.STORY_DOWNLOAD_FORMATS:
        mod, _, cls = name.rpartition('.')
        mod = import_module(mod)
        cls = getattr(mod, cls)
        yield cls()

def get_format(extension):
    for f in list_formats():
        if f.extension == extension:
            return f