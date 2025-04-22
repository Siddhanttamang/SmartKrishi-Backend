from flask import Blueprint, request, jsonify
from app.utils.weather import get_weather

weather_bp = Blueprint('weather_bp', __name__)
@weather_bp.route('/', methods=['GET'])
def weather():
    city = request.args.get('city', 'Kathmandu')  # Default city
    try:
        weather_info = get_weather(city)
        return jsonify(weather_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
