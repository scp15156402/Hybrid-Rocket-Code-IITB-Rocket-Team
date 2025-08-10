# app.py

from flask import Flask, render_template

from rocket_simulations.hybrid_rocket.hybrid_app import create_app as create_hybrid_app
from rocket_simulations.solid_rocket.solid_app import create_app as create_solid_app
from rocket_simulations.liquid_rocket.liquid_app import create_app as create_liquid_app

app = Flask(__name__)

@app.route("/")
def index():
    """Landing page to choose rocket simulation type."""
    return render_template("index.html")

# Register Hybrid rocket simulation under /hybrid_simulations
app.register_blueprint(
    create_hybrid_app().blueprints["hybrid"],
    url_prefix="/hybrid_simulations"
)

# Register Solid rocket simulation under /solid
app.register_blueprint(
    create_solid_app().blueprints["solid"],
    url_prefix="/solid"
)

# Register Liquid rocket simulation under /liquid
app.register_blueprint(
    create_liquid_app().blueprints["liquid"],
    url_prefix="/liquid"
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
