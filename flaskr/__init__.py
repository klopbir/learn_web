import os

from flask import Flask



def create_app(test_config=None):                   # In programming, a factory is a function (or class) whose job is to
                                                    # create and configure objects — instead of having those objects created at the top level of your code.
                                                    # so this is a factory because it sets up the Flask object
                                                    # this makes u able to create same different app objects so that they can be reused as materials for your run cases
                                                    # in the create_app u register the blueprints
    app = Flask(__name__, instance_relative_config=True)  # by default looks for either global app variable or create_app function in any module
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # app instance path is where Flask chose the main dir and flaskr.sqlite is the name of file
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) # load configs from config.py if it exists
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import auth

    app.register_blueprint(auth.bp)

    @app.route('/hello') # when u put decorator log it called log(func) and now when u put app.route it will call app.route('/hello')(func) app is the object route is its method
    def hello():         # u need this kind of decorator because u want your decorator to execute at definition and add this to the address side
        return '<a style="color:red">Hello World!</a>'

    # class Flask:
    #     def route(self, rule, **options):
    #         def decorator(func):
    #             # Register the function as a route handler
    #             self.add_url_rule(rule, func.__name__, func, **options)
    #             return func
    #
    #         return decorator

        # decorator is later called like decorator(func) ,, !! stores self in the closure so the function self.add... still works on app
    from . import db

    db.init_app(app)

    return app

