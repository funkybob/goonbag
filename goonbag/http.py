
import http.client
import re
from collections import OrderedDict


# Add some missing HttpResponse sub-classes
STATUS_CODES = list(http.client.responses.items()) + [
    (308, 'PERMANENT REDIRECT'),
    (427, 'BAD GEOLOCATION'),
]
STATUS_CODES = tuple(sorted(STATUS_CODES))

STATUS = OrderedDict(STATUS_CODES)
# Set constant-like properties for reverse lookup
for code, label in STATUS_CODES:
    setattr(STATUS, re.sub(r'\W', '_', label.upper()), code)
