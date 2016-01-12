import unittest
from onhands.hooks import Hook
from onhands.model import Model
from alabama.models import StringProperty


class UserHookUseless(Hook):
    pass


class UserWithUselessHook(Model):
    hooks = [UserHookUseless]


class UserHookException(Hook):
    def pre_save(self, user):
        raise Exception('Any exception %s' % (user.name,))


class UserHookFalse(Hook):
    def pre_save(self, user):
        return False


class UserHookTrue(Hook):
    def pre_save(self, user):
        return True


class User(Model):
    hooks = [UserHookException]

    name = StringProperty()


class AnotherUser(Model):
    hooks = [UserHookFalse]


class UserWithTwoHooks(Model):
    hooks = [UserHookTrue, UserHookFalse]


class TestHookBeforeSave(unittest.TestCase):

    def test_before_save_hook_case_exception(self):
        user = User(name='felipe')
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'Any exception felipe')

    def test_before_save_hook_return_false(self):
        user = AnotherUser()
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'The hook UserHookFalse.pre_save didnt return True')

    def test_before_save_hook_with_two_hooks(self):
        user = UserWithTwoHooks()
        with self.assertRaises(Exception) as e:
            user.put()
        self.assertEqual(str(e.exception), 'The hook UserHookFalse.pre_save didnt return True')

    def test_list_methods(self):
        self.assertEqual(UserHookUseless.methods, ['pre_save', 'pos_save', 'pre_delete'])

    def test_hook_pre_save_not_implemented(self):
        user = UserWithUselessHook()
        with self.assertRaises(NotImplementedError):
            user.put()


class UserDeleteHookTrue(Hook):
    def before_delete(self, user):
        return bool(user.name)


class UserDelete(Model):
    hooks = [UserDeleteHookTrue]
    name = StringProperty()


class TestHookBeforeDelete(unittest.TestCase):

    def test_before_delete_exception(self):
        u = UserDelete()
        with self.assertRaises(Exception) as e:
            u.delete()
        self.assertEqual(str(e.exception), 'The hook UserDeleteHookTrue.before_delete didnt return True')

    def test_before_delete(self):
        u = UserDelete(name="pythononhands")
        self.assertTrue(u.delete())
