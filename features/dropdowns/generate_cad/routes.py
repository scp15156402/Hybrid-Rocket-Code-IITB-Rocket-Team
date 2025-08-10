# features/dropdowns/generate_cad/routes.py

import os
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from .logic import generate_cad_parts

bp = Blueprint(
    "generate_cad",
    __name__,
    url_prefix="/dropdowns/generate_cad",
    template_folder="templates",
    static_folder="static/dropdowns",
)

@bp.route("/")
def page():
    """Render the Generate CAD UI."""
    return render_template("generate_cad.html")

@bp.route("/export", methods=["POST"])
def export():
    """Generate CAD parts and return download links."""
    data = request.get_json()
    current_values = data.get("current_values", {})
    results = data.get("results", {})

    cad_dir = os.path.join(current_app.root_path, "static", "cad")
    os.makedirs(cad_dir, exist_ok=True)

    files = generate_cad_parts(current_values, results, cad_dir)

    return jsonify(success=True, files=files)
