from .http import STATUS
from .utils import HeaderDict


class Response(Exception):
    '''
    A sub-class of Exception, allowing us to raise/catch it.

    With thanks to schinkel's repose.
    '''
    def __init__(self, status, content, headers):
        self.status = status
        self.content = content
        self.headers = HeaderDict(headers)

    def __getitem__(self, key):
        return self.headers[key]

    def __setitem__(self, key, value):
        self.headers[key] = value

    def __iter__(self):
        return iter(self.content)

#
# Success Responses (2xx)
#


class HttpResponseSuccess(Response):
    '''A base class for all 2xx responses, so we can issubclass test.'''


class OK(HttpResponseSuccess):
    status_code = STATUS.OK


class Created(HttpResponseSuccess):
    status_code = STATUS.CREATED


class Accepted(HttpResponseSuccess):
    status_code = STATUS.ACCEPTED


class NoContent(HttpResponseSuccess):
    status_code = STATUS.NO_CONTENT


class ResetContent(HttpResponseSuccess):
    status_code = STATUS.RESET_CONTENT


class PartialContent(HttpResponseSuccess):
    status_code = STATUS.PARTIAL_CONTENT

#
# Redirection Responses (3xx)
#


class HttpResponseRedirection(Response):
    '''A base class for all 3xx responses.'''


class LocationHeaderMixin:
    '''Many 3xx responses require a Location header'''
    def __init__(self, location, *args, **kwargs):
        self['Location'] = location

    url = property(lambda self: self['Location'])


class MultipleChoices(HttpResponseRedirection):
    status_code = STATUS.MULTIPLE_CHOICES


class MovedPermanently(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.MOVED_PERMANENTLY


class Found(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.FOUND


class SeeOther(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.SEE_OTHER


class NotModified(HttpResponseRedirection):
    status_code = STATUS.NOT_MODIFIED


class UseProxy(LocationHeaderMixin, HttpResponseRedirection):
    status_code = STATUS.USE_PROXY


class TemporaryRedirect(HttpResponseRedirection):
    status_code = STATUS.TEMPORARY_REDIRECT


class PermanentRedirect(HttpResponseRedirection):
    status_code = STATUS.PERMANENT_REDIRECT

#
# Common ancestor for 4xx and 5xx responses
#


class HttpResponseError(Response):
    '''Common base class for all error responses'''

#
# Client Error Responses (4xx)
#


class HttpResponseClientError(HttpResponseError):
    '''A base class for all 4xx responses.'''


class BadRequest(HttpResponseClientError):
    status_code = STATUS.BAD_REQUEST


# XXX Auth-Realm ?
class Unauthorized(HttpResponseClientError):
    status_code = STATUS.UNAUTHORIZED


class PaymentRequired(HttpResponseClientError):
    status_code = STATUS.PAYMENT_REQUIRED


class Forbidden(HttpResponseClientError):
    status_code = STATUS.FORBIDDEN


class NotFound(HttpResponseClientError):
    status_code = STATUS.NOT_FOUND


class MethodNotAllowed(HttpResponseClientError):
    def __init__(self, permitted_methods, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['Allow'] = ', '.join(permitted_methods)

    status_code = STATUS.METHOD_NOT_ALLOWED


class NotAcceptable(HttpResponseClientError):
    status_code = STATUS.NOT_ACCEPTABLE


class ProxyAuthenticationRequired(HttpResponseClientError):
    status_code = STATUS.PROXY_AUTHENTICATION_REQUIRED


class RequestTimeout(HttpResponseClientError):
    status_code = STATUS.REQUEST_TIMEOUT


class Conflict(HttpResponseClientError):
    status_code = STATUS.CONFLICT


class Gone(HttpResponseClientError):
    status_code = STATUS.GONE


class LengthRequired(HttpResponseClientError):
    status_code = STATUS.LENGTH_REQUIRED


class PreconditionFailed(HttpResponseClientError):
    status_code = STATUS.PRECONDITION_FAILED


class RequestEntityTooLarge(HttpResponseClientError):
    status_code = STATUS.REQUEST_ENTITY_TOO_LARGE


class RequestURITooLong(HttpResponseClientError):
    status_code = STATUS.REQUEST_URI_TOO_LONG


class UnsupportedMediaType(HttpResponseClientError):
    status_code = STATUS.UNSUPPORTED_MEDIA_TYPE


class RequestedRangeNotSatisfiable(HttpResponseClientError):
    status_code = STATUS.REQUESTED_RANGE_NOT_SATISFIABLE


class ExpectationFailed(HttpResponseClientError):
    status_code = STATUS.EXPECTATION_FAILED


class BadGeolocation(HttpResponseClientError):
    status_code = STATUS.BAD_GEOLOCATION

#
# Server Error (5xx)
#


class HttpResponseServerError(HttpResponseError):
    '''A base class for 5xx responses.'''


class InternalServerError(HttpResponseServerError):
    status_code = STATUS.INTERNAL_SERVER_ERROR


class NotImplemented(HttpResponseServerError):
    status_code = STATUS.NOT_IMPLEMENTED


class BadGateway(HttpResponseServerError):
    status_code = STATUS.BAD_GATEWAY


class ServiceUnavailable(HttpResponseServerError):
    status_code = STATUS.SERVICE_UNAVAILABLE


class GatewayTimeout(HttpResponseServerError):
    status_code = STATUS.GATEWAY_TIMEOUT


class HttpVersiontNotSupported(HttpResponseServerError):
    status_code = STATUS.HTTP_VERSION_NOT_SUPPORTED
