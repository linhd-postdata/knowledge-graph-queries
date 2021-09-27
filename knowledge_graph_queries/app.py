#!/usr/bin/python
import os
import connexion

app = connexion.App(__name__, options={"swagger_ui": True})
if __name__ == "__main__":  # pragma: no cover
    app.run(port=os.environ.get("PORT", 5000), specification_dir='openapi/')
