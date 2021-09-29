#!/usr/bin/python
import os
import connexion
from flask import g


app = connexion.App(__name__, options={"swagger_ui": True})


@app.app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == "__main__":  # pragma: no cover
    app.run(port=os.environ.get("PORT", 5000), specification_dir='openapi/')
