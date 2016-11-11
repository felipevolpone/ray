
class DatabaseHook(object):

    methods = ['before_save', 'before_delete', 'after_save']

    def before_save(self, entity):
        """
            before_save it's the final moment before the entity being save.
            if the methods return true, the entity will be saved, if doesnt
            will not.
        """
        return True

    def before_delete(self, entity):
        """
            before_delete it's the moment right before the entity is deleted.
            the entity will only be removed if this method returns true.
        """
        return True

    def after_save(self, entity):
        """
            after_save it's the moment after the entity is saved.
        """
        pass
