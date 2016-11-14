
class RayException(Exception):
    http_code = None

    def __init__(self, *args, **kwargs):
        super(RayException, self).__init__(*args, **kwargs)


class ModelNotFound(RayException):
    http_code = 404


class Forbidden(RayException):
    http_code = 403


class MethodNotFound(RayException):
    http_code = 404


class NotAuthorized(RayException):
    http_code = 401


class ShieldDoNotHaveModel(RayException):
    http_code = 500


class PutRequiresIdOnJson(RayException):
    http_code = 502


class BadRequest(RayException):
    http_code = 502


class HookException(RayException):
    http_code = 400


class EndpointNotFound(RayException):
    http_code = 404


class AuthenticationExpirationTime(RayException):
    http_code = 500


class ActionUnderAuthenticationProtection(RayException):
    http_code = 403


class MethodUnderShieldProtection(RayException):
    http_code = 404
