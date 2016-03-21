# Ray :saxophone:

Ray is a framework that helps you to deliver well-designed software without been stucked in your framework. Ray it's a ready to production framework that contains a uWSGI server ready to be used on production enviroment.

[![Build Status](https://travis-ci.org/felipevolpone/ray.svg?branch=master)](https://travis-ci.org/felipevolpone/ray)
[![Coverage Status](https://coveralls.io/repos/felipevolpone/ray/badge.svg?branch=master&service=github)](https://coveralls.io/github/felipevolpone/ray?branch=master)
[![Code Climate](https://codeclimate.com/github/felipevolpone/ray/badges/gpa.svg)](https://codeclimate.com/github/felipevolpone/ray)

## Features

### Easy APIs
Create a model and then decorated it with the endpoint decorator.
```python
from ray.endpoint import endpoint
from ray_sqlalchemy import AlchemyModel
from sqlalchemy import Column, Integer, String

Base = declarative_base()

@endpoint('/user')
class UserModel(AlchemyModel):
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
from ray.hooks import Hook

class AgeValidationHook(Hook):
    def before_save(self, user):
        if user.age < 18:
            raise Exception('The user must have more than 18 years')
        return True

@endpoint('/user')
class UserModel(AlchemyModel):
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
from ray.actions import ActionAPI, action

class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("/activate")
    def activate_user(self, model_id):
        user = storage.get(UserModel, model_id)
        user.activate = True
        storage.put(user)
```

### Authentication
Ray has a built-in authentication module. To use it, you just need to inherit the Authentication class and implement the method authenticate, that will check the data in the database and then return if the user can login or not. Remember that this method must return a dictionary if the authentication succeeded.

```python
from ray.authentication import Authentication


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        user = User.query(User.username == username, User.password == password).one()
        return {'username': 'ray'} if user else None
```

Now, you can just add this to your endpoint:
```python
@endpoint('/person', authentication=MyAuth)
class PersonModel(ModelInterface):
    pass
```

Then, your model endpoint is protected. To use it, you need to login. To login:
```python
import request
request.post('http://localhost:8080/api/login', data={"username": "yourusername", "password": "yourpassword"})
```


### Running server
Ray runs a WSGI server to serve your application. Also, you can just run the command bellow and starting writing your business rules. The option *--wsgifile*, must be used to tell to Ray in which file it should find your *application* scope.

```python
# app.py file
from ray.wsgi.wsgi import application
```

```bash
ray up --wsgifile=app.py
```

## Integration with

### SQLAlchemy
You can use all features of SQLAlchemy with Ray.


## FAQ
**Is Ray a MVC framework?**
- No!

## Development
**To run the tests**
```bash
py.test tests/
```

## TO DO
- [ ] Shields
- [ ] SQLAlchemy Integration - Where param at url
- [ ] Decorators to return Content-Type: html and csv.
- [ ] HTTP Task Queue
- [ ] HTTP Mail Service
- [ ] Google App Engine
- [ ] Request Middleware (like Django)
- [ ] API versions
