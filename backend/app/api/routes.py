from flask import Blueprint, request, jsonify
from app.services.sector_service import generate_sectors_from_ipp

api = Blueprint("api", __name__, url_prefix="/api")

@api.route('/generate-sectors', methods=['POST'])
def generate_sectors():
    """
    API endpoint that generates sectors based on the provided IPP.
    """
    data = request.get_json()
    ipp = data.get('ipp')

    results = generate_sectors_from_ipp(ipp)
    return jsonify(results)