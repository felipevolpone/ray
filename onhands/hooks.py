
class Hook(object):

    methods = ['pre_save', 'pos_save', 'pre_delete']

    def pre_save(self, entity):
        """
            pre_save it's the final moment before the entity being save.
            if the methods return true, the entity will be saved, if doesnt
            will not.
        """
        raise NotImplementedError

    def pos_save(self, entity):
        raise NotImplementedError

    def pre_delete(self, entity):
        raise NotImplementedError
