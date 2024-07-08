from quart import Quart
 # Import routes module

app = Quart(__name__, template_folder='../templates', static_folder='../static')


app.config["DEBUG"] = True  # Enable debug mode



# Ensure that Quart recognizes this module as a package
__all__ = ['app']

from . import routes  # Import the routes defined in `routes.py`

