from flask import Flask
from .schema import schema
from flask_graphql import GraphQLView
from .extensions import db_session

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

app.add_url_rule("/graphql", 
                    view_func=GraphQLView.as_view(
                        "graphql",
                        graphiql=True,
                        schema=schema
                    ))



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(debug=True)