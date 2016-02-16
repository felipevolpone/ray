# Python on Hands

Python on Hands is a framework that helps you to deliver well designed software without been stucked in your framework. On Hands it's a ready to production framework that contains a uWSGI server that can be used in production as well.

[![Build Status](https://travis-ci.org/felipevolpone/onhands.svg?branch=master)](https://travis-ci.org/felipevolpone/onhands)
[![Coverage Status](https://coveralls.io/repos/felipevolpone/onhands/badge.svg?branch=master&service=github)](https://coveralls.io/github/felipevolpone/onhands?branch=master)
[![Code Climate](https://codeclimate.com/github/felipevolpone/onhands/badges/gpa.svg)](https://codeclimate.com/github/felipevolpone/onhands)

## Features

### Easy APIs
Create a model and then decorated it with the endpoint decorator.
```python
from onhands.endpoint import endpoint
from onhandsalabama import AlabamaModel
from alabama import StringProperty, IntegerProperty

@endpoint('/user')
class UserModel(AlabamaModel):
    name = StringProperty()
    age = IntegerProperty()
```
Now, you have the http methods to interact with your model using the urls:

|HTTP Verb | Path | Description          |
|--------- | ---- | -------------------- |
|  GET     | /user| List all users       |
|  GET     | /user/{id} | Get one user   |
|  POST    | /user| Create an user       |
|  PUT     | /user/{id} | Update an user |
|  DELETE  | /user/{id} | Delete an user |


### Hooks
Hooks are really useful to add validations in different moments of your application. Hook is a class that connect with your model and will be executed **before save the model, after the model be saved or before the model be deleted**.
```python
from onhands.hooks import Hook

class AgeValidationHook(Hook):
    def before_save(self, user):
        if user.age < 18:
            raise Exception('The user must have more than 18 years')
        return True

@endpoint('/user')
class UserModel(Model):
    hooks = [AgeValidationHook]
    name = StringProperty()
    age = IntegerProperty()
```
| Available Hooks |
| --------------- |
|  before_delete  |
|  before_save    |


Then, if you call the .put() method of UserModel and the user doesn't has age bigger than 18, an Exception will be raised.

### Actions
Actions provide a simple way to you create behavior in your models through your api. After writing the code bellow, you can use the url */api/user/< id >/activate* to invoke the activate_user method.
```python
from onhands.actions import ActionAPI, action

class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("/activate")
    def activate_user(self, model_id):
        user = storage.get(UserModel, model_id)
        user.activate = True
        storage.put(user)
```

### Running server
OnHands runs a WSGI server to serve your application. Also, you can just run the command bellow and starting writing your business rules. The option *--wsgifile*, must be used to tell to OnHands in which file it should find your *application* scope.

```python
# app.py file
from onhands.wsgi.wsgi import application
```

```bash
onhands up --wsgifile=app.py
```

## Integration with

### Alabama
OnHands works perfectly with [Alabama](http://github.com/felipevolpone/alabama_orm). You can see an example on onhands-alabama directory.

## FAQ
**Is Python On Hands a MVC framework?**
- No!

## Development
**To run the tests**
```bash
py.test tests/
```

## TO DO
[ ] SQLAlchemy Integration - Where param at url
[x] SQLAlchemy Integration
[ ] Authentication
[ ] Request Middleware (like Django)
[ ] Google App Engine
[ ] HTTP Task Queue
[ ] HTTP Mail Service
[ ] SQLAlchemy Integration
[ ] API versions
[ ] Python 3 compability
[ ] Decorators to return Content-Type: html and csv.
