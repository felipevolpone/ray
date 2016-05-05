# Ray :saxophone:

Ray is a framework that helps you to deliver well-designed software without been stuck in your framework. Ray it's a ready to production framework that contains a uWSGI server ready to be used on production environment.

[![Build Status](https://travis-ci.org/felipevolpone/ray.svg?branch=master)](https://travis-ci.org/felipevolpone/ray)
[![Coverage Status](https://coveralls.io/repos/felipevolpone/ray/badge.svg?branch=master&service=github)](https://coveralls.io/github/felipevolpone/ray?branch=master)
[![Code Climate](https://codeclimate.com/github/felipevolpone/ray/badges/gpa.svg)](https://codeclimate.com/github/felipevolpone/ray)

## Features

* Easy APIs
* Database Hooks
* Authentication
* Protecting API
* uWSGI built-in server
* Integration with SQLAlchemy

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
Actions provide a simple way to you create behavior in your models through your api. After writing the code bellow, you can use the url */api/user/<id>/activate* to invoke the activate_user method.
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
Ray has a built-in authentication module. To use it, you just need to inherit the Authentication class and implement the method *authenticate*. In this method, you'll check the data in the database and then return if the user can login or not. Remember that this method must return a dictionary if the authentication succeeded.

```python
from ray.authentication import Authentication


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        user = User.query(User.username == username, User.password == password).one()
        return {'username': 'ray'} if user else None
```

If you want protect all the operations in this endpoint, you can just add this:
```python
@endpoint('/person', authentication=MyAuth)
class PersonModel(ModelInterface):
    pass
```

Then, your model endpoint is protected. To use it, you need to login.
```python
import request
request.post('http://localhost:8080/api/_login', data={"username": "yourusername", "password": "yourpassword"})
```

### Shields
Ray has an option to you protect your API: using Shields. How it works? You inherit from the Shield class and implement just the http method that you *want to protect*.

```python
class PersonShield(Shield):
    __model__ = PersonModel

    def get(self, info):
        return info['profile'] == 'admin'

    # def put(self, info): pass

    # def post(self, info): pass

    # def delete(self, info): pass
```
This shield protects the GET method of /api/person. The parameter *info* in the get method on the shield, is the dictionary returned on your Authentication class. So, all Shields's methods receive this parameter. When you overwrite
a method, Ray will assume that method is under that Shield protection.

### Shields with Actions
If you wanna to protect an action you can do this with Shield. To do this, you just need to implement a @classmethod method in your Shield, *that doesnt has one of these names: get, delete, post or put*.
If this Action is not used by an authenticated user, the parameter info in your Shiled's method will be None.

```python

class UserShield(Shield):
    __model__ = UserModel

    @classmethod
    def protect_enable(cls, info):
        return info['profile'] == 'admin'


class ActionUser(ActionAPI):
    __model__ = UserModel

    @action('/enable', protection=UserShield.protect_enable)
    def enable_user(self, model_id):
        user = session.get_user()
        user.enabled = True
        user.save()
```

### Running server
Ray has a WSGI server to run your application. To use it, you just need to run the command bellow and start writing your business rules. The command parameter *--wsgifile*, must be used to tell to Ray in which file it should find your *application* scope.

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
**Running the tests**
```bash
# inside the ray-core dir
py.test tests/
```

**to do list**
- [ ] Google App Engine Compability

**middle priority**
- [ ] Admin panel (like django-admin)
- [ ] Decorators to return Content-Type: html and csv.
- [ ] HTTP Task Queue
- [ ] HTTP Mail Service

**low priority**
- [ ] Request Middleware (like Django)
- [ ] API versions
