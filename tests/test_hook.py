import unittest
from onhands.hooks import Hook
from onhands.model import Model
from alabama.models import StringProperty


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


class TestHook(unittest.TestCase):

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
