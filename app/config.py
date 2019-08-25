from config import Configuration
app.config.from_object(Configuration)


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/test1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    