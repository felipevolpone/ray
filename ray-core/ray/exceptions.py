
class ModelNotFound(Exception):
    pass


class Forbidden(Exception):
    pass


class MethodNotFound(Exception):
    pass


class ActionDoNotHaveModel(Exception):
    pass


class NotAuthorized(Exception):
    pass


class ShieldDoNotHaveModel(Exception):
    pass


class PutRequiresIdOnJson(Exception):
    pass


class BadRequest(Exception):
    pass


class HookException(Exception):
    pass
