from flaskr import app, auth
from flaskr.models import User

@auth.verify_password
def verify_pw(username, password):
    user, checked = User.auth(username, password)
    return checked

from .idm import bp
app.register_blueprint(idm.bp)
