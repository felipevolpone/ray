
class Hook(object):

    methods = ['before_save', 'before_delete']

    def before_save(self, entity):
        """
            before_save it's the final moment before the entity being save.
            if the methods return true, the entity will be saved, if doesnt
            will not.
        """
        raise NotImplementedError

    def before_delete(self, entity):  # FIXME nao ta lancando excecao que nem o before_save
        raise NotImplementedError

    def after_save(self, entity):  # FIXME
        raise NotImplementedError
