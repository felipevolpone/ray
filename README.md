# Python on Hands

Python on Hands is framework that helps you to deliver well designed software without been stucked in your framework. On Hands it's a ready to production framework that contains a uWSGI server that can be used in production. 

## Features

### Easy APIs
Create a model and then decorated it with the endpoint decorator.
```python
from yawpy.endpoint import endpoint
from alabama import BaseModel, StringProperty, IntegerProperty

@endpoint('/user')
class UserModel(BaseModel):
    name = StringProperty()
    age = IntegerProperty()
```
Now, you have the http methods **post, put, get, delete** to interact with your model using the url: */api/user*

### Hooks
Hooks are really usefull to add validations in different moments of your application. Hook is a class that connect with your model and will be executed *before the model save, after the model be saved or before the model be deleted*.
```python
from yawpy.hooks import Hook

class AgeValidationHook(Hook):
    def pre_save(self, user):
        if user.age < 18:
            raise Exception('The user must have more than 18 years')
        return True

@endpoint('/user')
class UserModel(Model):
    hooks = [AgeValidationHook]
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()
```
Then, if you call the .put() method of usermodel and the user doesn't has age bigger than 18, an Exception will be raised.

## Development

#### To run the tests
```bash
py.test tests/
```