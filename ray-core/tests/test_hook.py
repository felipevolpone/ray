import unittest
from ray.hooks import DatabaseHook
from ray.model import Model


class UserHookUseless(DatabaseHook):
    pass


class UserWithUselessHook(Model):
    hooks = [UserHookUseless]


class UserHookException(DatabaseHook):
    def before_save(self, user):
        raise Exception('Any exception %s' % (user.name,))


class UserHookFalse(DatabaseHook):
    def before_save(self, user):
        return False


class UserHookFalse2(DatabaseHook):
    def before_save(self, user):
        return False


class UserHookTrue(DatabaseHook):
    def before_save(self, user):
        return True


class User(Model):
    hooks = [UserHookException]

    def __init__(self, name=None):
        self.name = name


class UserWithTwoHooks(Model):
    hooks = [UserHookFalse2, UserHookTrue, UserHookFalse]


class TestHookBeforeSave(unittest.TestCase):

    def test_before_save(self):
        class UserRight(Model):
            hooks = [UserHookTrue]

        user = UserRight()
        self.assertTrue(user.put())

    def test_before_save_hook_failing(self):
        user = User(name='felipe')
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'Any exception felipe')

    def test_before_save_hook_with_two_hooks(self):
        user = UserWithTwoHooks()
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'The hook(s) UserHookFalse2, UserHookFalse.before_save didnt return True')

    def test_hook_before_save_not_implemented(self):
        user = UserWithUselessHook()
        self.assertTrue(user.put())
        self.assertTrue(user.delete())


class UserDeleteHookTrue(DatabaseHook):
    def before_delete(self, user):
        return bool(user.name)


class UserDeleteHookFalse(DatabaseHook):
    def before_delete(self, user):
        return False


class UserDelete(Model):
    hooks = [UserDeleteHookTrue]

    def __init__(self, name=None):
        self.name = name


class UserDeleteFailing(Model):
    hooks = [UserDeleteHookTrue, UserDeleteHookFalse]

    def __init__(self, name=None):
        self.name = name


class TestHookBeforeDelete(unittest.TestCase):

    def test_before_delete_exception(self):
        u = UserDelete()
        with self.assertRaises(Exception) as e:
            u.delete()
        self.assertEqual(str(e.exception), 'The hook(s) UserDeleteHookTrue.before_delete didnt return True')

    def test_before_delete(self):
        u = UserDelete(name="ray")
        self.assertTrue(u.delete())

    def test_before_delete_fail(self):
        u = UserDeleteFailing()
        with self.assertRaises(Exception) as e:
            u.delete()

        self.assertEqual(str(e.exception), 'The hook(s) UserDeleteHookTrue, UserDeleteHookFalse.before_delete didnt return True')

    def test_before_delete_not_implemented(self):
        class UserDeleteHookTrue(DatabaseHook):
            pass

        class UserDelete(Model):
            hooks = [UserDeleteHookTrue]

        u = UserDelete()
        self.assertTrue(u.delete())


class UserAfterSaveHook(DatabaseHook):
    def before_save(self, user):
        return True

    def after_save(self, user):
        user.name = 'modified'


class UserAfterSave(Model):
    hooks = [UserAfterSaveHook]

    def __init__(self, name=None):
        self.name = name


class TestHookAfterSave(unittest.TestCase):

    def test_after_save(self):
        u = UserAfterSave(name='ray')
        u.put()

        self.assertEqual('modified', u.name)

    def test_after_save_not_implemented(self):
        class UserAfterSaveUselessHook(DatabaseHook):
            pass

        class UserAfterSaveUseless(Model):
            hooks = [UserAfterSaveUselessHook]

        u = UserAfterSaveUseless()
        self.assertTrue(u.put())
