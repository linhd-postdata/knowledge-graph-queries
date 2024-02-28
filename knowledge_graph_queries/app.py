#!/usr/bin/python
import os
import connexion
from flask import g
from flask_cors import CORS
from connexion.resolver import MethodViewResolver

app = connexion.App(__name__, options={"swagger_ui": True})
app.add_api('openapi/openapi.yml', strict_validation=True)
CORS(app.app)

@app.app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()

if __name__ == "__main__":  # pragma: no cover
    app.run(port=os.environ.get("PORT", 5005), specification_dir='./openapi/', debug=True)
