from flask import request, jsonify
from flask.blueprints import Blueprint

from app.extensions import db
from app.models.industry import Industry

import pandas
import json

# Define a blueprint for the industryFiles
industry_bp = Blueprint("industry", __name__, url_prefix="/industry")


# Flask routes for industryFiles operations
@industry_bp.route("/<string:filename>", methods=["GET"])
def get_json_statistic_data(
    filename,
):
    statistic_data = pandas.read_excel(
        "../../statistic-data/" + filename,
        sheet_name="Data",
    )
    json_data = statistic_data.to_json(orient="records")
    return json.dumps(json.loads(json_data))
