"""Entry point of this application."""
import os
from application import create_app
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from application.helpers import sorry

app = create_app()

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def errorhandler(e):
    """Handle error."""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return sorry("something is broken! Please consider reloading.", e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "main":
    app.run()
