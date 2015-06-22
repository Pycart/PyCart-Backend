# PyCart -  A Flexible solution for your e-commerce needs

This project is a robust and flexible e-commerce site built with [AngularJS](https://angularjs.org/) and [Django](https://www.djangoproject.com/).

## Project Set-up

To get you started you should clone down both the front and back Pycart repositories.

### Cloning the Front-End Repository
Once you have git installed, you can clone the front-end portion of this project down from the Pycart repository found on github.
```
git clone https://github.com/Pycart/PyCart-Frontend
```

#### Install Dependencies - AngularJS

There are multiple dependencies in this project: angular framework code, bootstrap, etc.

* You can install the tools via `npm`, the [node package manager][npm].
* You can install the angular code via `bower`, a [client-side code package manager][bower].

Both `npm` and  `bower`  are configured to automatically run upon typing:

```
npm install
```

This also calls `bower install` which will create two new folders in your project:

* `node_modules` - contains the npm packages
* `app/bower_components` - contains the angular framework files

#### Run Front-end During Development

You can start the server by typing:
```
npm start
```
You can now browse to the app locally at `http://localhost:8000/app/index.html`.

This project also comes a local development web server. You can start this web server by using `npm start`:

```
sudo npm install
```

Then you can choose to configure your own webserver, such as apache or nginx. Just configure your server to serve the files under the `app/` directory.


### Cloning the Back-End Repository
You can clone the front-end portion of this project down from the Pycart repository found on github.
```
git clone https://github.com/Pycart/PyCart-Backend
```

#### Install Dependencies - Django

Before you install your dependencies, you will need to install your virtual environment, virtual environment wrapper and pip. We suggest using the combined installer found on brainsik's github account under [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito). Once inside of your virtual environment, you can install the dependencies found in the requirements.txt file.
```
(yourvrtenv) $ pip install django
(yourvrtenv) $ pip freeze > requirements.txt
```
The requirements.txt contains a variety of dependencies necessary for full functionality of this project. A few of the key dependencies are listed and further explained below:

- djoser = User authentication based on the Django user authentication
- stripe = Payment processing tools
- Pillow = Imaging tools
- wheel = Packaging, compressing and installation of Python packages
- six = Cross Compatibility between Python 2 and 3
- django-taggit = Provides robust tagging capabilities for items

## User Authentication and Admin access
### User Authentication
This app contains user authentication based on djoser, which is a REST implementation of the built-in Django user authentication module. This allows for a basic separation between the e-commerce user and admin.

### Admin Access
A key feature of this project is the Admin access. An admin would be person in charge of maintaining and updating items on their e-commerce site.  As an admin of an e-commerce site, you would have a variety of abilities:

- Item management = Add new item to be displayed to users
- Order management = View current orders
- Status management = View current status options
- User management = View current users

We are constantly updating and expanding our admin capabilities, so any suggestions or feedback that you may have is more than welcome.

## We hope you enjoy this open source e-commerce platform!

[git]: http://git-scm.com/
[bower]: http://bower.io
[npm]: https://www.npmjs.org/
[node]: http://nodejs.org

