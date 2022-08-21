from lib2to3.pgen2.pgen import generate_grammar
from flask.testing import FlaskClient
import flask
from flask_wtf.csrf import generate_csrf

"""
Classes for testing with CSRF protection enabled
"""
class CSRF_wrapper(object):
    def __init__(self, client):
        self.client = client
        self.vary = set({})

    def set_cookie(self, key, value='', *args, **kwargs):
        server_name = flask.current_app.config['SERVER_NAME'] or 'localhost'
        return self.client.set_cookie(
            server_name, key=key, value=value, *args, **kwargs
        )

    def delete_cookie(self, key, *args, **kwargs):
        "Delete the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.delete_cookie(
            server_name, key=key, *args, **kwargs
        )


class NewFlaskClient(FlaskClient):
    @property
    def csrf_token(self):
        request = CSRF_wrapper(self)

        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)
        with self.application.test_request_context(
            "/login", environ_overrides=environ_overrides
        ):
            csrf_token = generate_csrf()
            print(csrf_token)
            flask.current_app.session_interface.save_session(self.application, flask.session, request)
            return csrf_token
    
    def login(self, username, password):
        print(self.csrf_token)
        return self.post("/login", 
        headers={
            "X-CSRFToken": self.csrf_token
        },
        json={
            "username": username,
            "password": password
        })

    def logout(self):
        return self.get("/logout", follow_redirects=True)



