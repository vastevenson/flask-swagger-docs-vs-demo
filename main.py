from flask import Flask
from flask_restful import Api, Resource, reqparse
import datetime
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


api = Api(app)

new_user_post_args = reqparse.RequestParser()
new_user_post_args.add_argument("name",
                                type=str,
                                help="You must input a name.",
                                required=True)

new_user_post_args.add_argument("age",
                                type=int,
                                help="You must specify the age for a given name.",
                                required=False)


class New_User(Resource):
    def post(self):
        args = new_user_post_args.parse_args()
        age = args['age']
        name = args['name']
        now = datetime.datetime.now()
        response = {
            'name': name,
            'age': age,
            'created_on': now.strftime("%m/%d/%Y, %H:%M:%S")
        }
        return response


api.add_resource(New_User, "/api/new_user")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# http://localhost/api/new_user
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)