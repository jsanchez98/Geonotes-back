import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    DEBUG=True
    SESSION_COOKIE_HTTPONLY=True
    REMEMBER_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Lax"
    SESSION_COOKIE_SECURE=True
    SECRET_KEY="secreto"
    #SESSION_COOKIE_SECURE=False
    #WTF_CSRF_SECRET_KEY="secreto"
