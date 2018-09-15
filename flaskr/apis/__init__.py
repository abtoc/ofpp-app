from flaskr import app

from .idm import bp
app.register_blueprint(idm.bp)
