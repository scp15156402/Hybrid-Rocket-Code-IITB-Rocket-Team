import os
from flask import Flask, render_template
from flask_caching import Cache

from rocket_simulations.hybrid_rocket.hybrid_app import hybrid_bp
import rocket_simulations.hybrid_rocket.hybrid_app as hybrid_module
from rocket_simulations.hybrid_rocket.logic.plots import init_plot_cache

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)

# Configure cache
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
cache = Cache(app)
init_plot_cache(app)

# Wire this cache into the hybrid_app module
hybrid_module.cache = cache

@app.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(hybrid_bp, url_prefix="/hybrid_simulations")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
