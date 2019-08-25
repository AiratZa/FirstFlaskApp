from flask import Flask


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


from flask_security import SQLAlchemyUserDatastore, Security
from flask_security import login_required, current_user

from flask import redirect, url_for, request

app = Flask (__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Airat'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

db = SQLAlchemy(app)

migrate = Migrate (app, db)
manager = Manager(app)

manager.add_command ('db', MigrateCommand)

##### ADMIN
from models import *

class BaseModelView(ModelView):
    def on_model_change(self, form, model, created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, created)

class AdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')
    def inaccessible_callback(self, name,  **kwargs):
        return redirect( url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags' ]

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts' ]


admin = Admin(app, "FlaskAdmin", url ='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post,db.session))
admin.add_view(TagAdminView(Tag,db.session))


### FLASK SECURITY ###

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

