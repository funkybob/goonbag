'''
Handle abstraction to find the 'best' available JSON lib
'''

try:
    import simplejson as json  # NOQA
except ImportError:
    import json  # NOQA
