import redis
import flask
from views import views

app = flask.Flask(__name__)

app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=False)